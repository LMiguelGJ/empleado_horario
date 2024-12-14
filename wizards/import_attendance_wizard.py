from odoo import models, fields, _
from odoo.exceptions import UserError
import csv
from io import StringIO
from datetime import datetime
import base64


class ImportAttendanceWizard(models.TransientModel):
    _name = 'import.attendance.wizard'
    _description = 'Wizard to Import Attendance Data'

    file = fields.Binary(string="Archivo CSV", required=True)
    filename = fields.Char(string="Nombre del archivo")

    def procesar_registros(self):
        if not self.file:
            raise UserError(_("Por favor, suba un archivo CSV."))

        # Decodificar contenido del archivo
        contenido_csv = base64.b64decode(self.file).decode('utf-8')
        contenido_csv = contenido_csv.replace(';', ',')
        file_stream = StringIO(contenido_csv)
        reader = csv.reader(file_stream, delimiter=',')

        # Leer encabezados
        headers = next(reader, None)
        if not headers or len(headers) < 2:
            raise UserError(_("El archivo CSV debe tener al menos dos columnas: Fecha y Hora, y Nombre."))

        # Buscar encabezados específicos con coincidencias parciales
        fecha_index = next((i for i, h in enumerate(headers) if "data e hora" in h.lower()), None)
        nombre_index = next((i for i, h in enumerate(headers) if "nome (usuário)" in h.lower()), None)

        if fecha_index is None or nombre_index is None:
            # Si no se encuentran, usar las dos primeras columnas
            fecha_index, nombre_index = 0, 1

        registros = {}

        for row in reader:
            fecha_hora_str, nombre = row[fecha_index].strip(), row[nombre_index].strip() or "Desconocido"

            # Convertir fecha y hora a objeto datetime
            fecha_hora_str = fecha_hora_str.strip()
            try:
                fecha_hora = datetime.strptime(fecha_hora_str, '%d/%m/%Y %H:%M:%S')
            except ValueError:
                try:
                    fecha_hora = datetime.strptime(fecha_hora_str, '%d/%m/%Y %H:%M')
                except ValueError:
                    raise UserError(_("Formato de fecha/hora inválido en: %s. Use DD/MM/YYYY HH:MM:SS o DD/MM/YYYY H:MM." % fecha_hora_str))

            fecha = fecha_hora.date()

            # Inicializar estructura de datos para el empleado
            if nombre not in registros:
                registros[nombre] = {}

            if fecha not in registros[nombre]:
                registros[nombre][fecha] = []

            registros[nombre][fecha].append(fecha_hora)

        # Ordenar registros y determinar entrada y salida
        for nombre, dias in registros.items():
            for fecha, tiempos in dias.items():
                tiempos.sort()  # Ordena cronológicamente
                entrada = tiempos[0] if tiempos else None
                salida = tiempos[-1] if len(tiempos) > 1 else entrada

                if entrada and salida and salida < entrada:
                    raise UserError(_(
                        "La hora de salida no puede ser anterior a la hora de entrada para el empleado: %s en la fecha: %s. salida: %s - entrada: %s" % (nombre, fecha, salida, entrada)))

                registros[nombre][fecha] = {'entrada': entrada, 'salida': salida}

        # Crear registros de asistencia
        modelo_asistencias = self.env['hr.attendance']
        empleados = self.env['hr.employee'].sudo().search_read([], ['name', 'id'])
        mapa_empleados = {empleado['name']: empleado['id'] for empleado in empleados}

        for nombre, dias in registros.items():
            for fecha, tiempos in dias.items():
                entrada = tiempos['entrada']
                salida = tiempos['salida']

                # Validar o completar información
                if entrada and not salida:
                    salida = entrada
                elif salida and not entrada:
                    entrada = salida

                empleado_id = mapa_empleados.get(nombre)
                if not empleado_id:
                    nuevo_empleado = self.env['hr.employee'].sudo().create({'name': nombre})
                    empleado_id = nuevo_empleado.id
                    mapa_empleados[nombre] = empleado_id

                # Crear registro de asistencia
                modelo_asistencias.create({
                    'employee_id': empleado_id,
                    'date_in': entrada.date(),
                    'check_in': entrada,
                    'check_out': salida,
                })

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
