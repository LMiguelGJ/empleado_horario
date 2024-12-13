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
        file_stream = StringIO(contenido_csv)
        reader = csv.reader(file_stream, delimiter=',')

        # Leer encabezados
        headers = next(reader, None)
        if not headers or len(headers) < 2:
            raise UserError(_("El archivo CSV debe tener al menos dos columnas: Fecha y Hora, y Nombre."))

        # Buscar encabezados específicos con coincidencias parciales
        fecha_index = next((i for i, h in enumerate(headers) if "data" in h.lower() and "hora" in h.lower()), None)
        nombre_index = next((i for i, h in enumerate(headers) if "nome" in h.lower()), None)

        if fecha_index is None or nombre_index is None:
            # Si no se encuentran, usar las dos primeras columnas
            fecha_index, nombre_index = 0, 1

        registros = {}
        for row in reader:
            # if len(row) < 2:
            #     continue  # Ignorar filas incompletas

            fecha_hora_str, nombre = row[fecha_index].strip(), row[nombre_index].strip() or "Desconocido"

            # Convertir fecha y hora a objeto datetime
            try:
                fecha_hora = datetime.strptime(fecha_hora_str, '%m/%d/%Y %H:%M')
            except ValueError:
                raise UserError(_("Formato de fecha/hora inválido en: %s. Use MM/DD/YYYY HH:MM." % fecha_hora_str))

            fecha = fecha_hora.date()

            # Inicializar estructura de datos para el empleado
            if nombre not in registros:
                registros[nombre] = {}

            if fecha not in registros[nombre]:
                registros[nombre][fecha] = {'entrada': None, 'salida': None}

            # Determinar si es entrada o salida
            if fecha_hora.hour < 12:  # Entrada
                if registros[nombre][fecha]['entrada'] is None or fecha_hora < registros[nombre][fecha]['entrada']:
                    registros[nombre][fecha]['entrada'] = fecha_hora
            else:  # Salida
                if registros[nombre][fecha]['salida'] is None or fecha_hora > registros[nombre][fecha]['salida']:
                    registros[nombre][fecha]['salida'] = fecha_hora

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
