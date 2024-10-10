# empleado_horario/models/empleado.py
from odoo import models, fields

class Empleado(models.Model):
    _name = 'empleado.horario'
    _description = 'Registro de Empleados y Horarios'

    nombre = fields.Char(string='Nombre del Empleado', required=True)
    lunes_labora = fields.Boolean(string='Laborable')
    lunes_entrada = fields.Datetime(string='Hora Entrada Lunes')
    lunes_salida = fields.Datetime(string='Hora Salida Lunes')
    
    martes_labora = fields.Boolean(string='Laborable')
    martes_entrada = fields.Datetime(string='Hora Entrada Martes')
    martes_salida = fields.Datetime(string='Hora Salida Martes')
    
    miercoles_labora = fields.Boolean(string='Laborable')
    miercoles_entrada = fields.Datetime(string='Hora Entrada Miércoles')
    miercoles_salida = fields.Datetime(string='Hora Salida Miércoles')
    
    jueves_labora = fields.Boolean(string='Laborable')
    jueves_entrada = fields.Datetime(string='Hora Entrada Jueves')
    jueves_salida = fields.Datetime(string='Hora Salida Jueves')
    
    viernes_labora = fields.Boolean(string='Laborable')
    viernes_entrada = fields.Datetime(string='Hora Entrada Viernes')
    viernes_salida = fields.Datetime(string='Hora Salida Viernes')
    
    sabado_labora = fields.Boolean(string='Laborable')
    sabado_entrada = fields.Datetime(string='Hora Entrada Sábado')
    sabado_salida = fields.Datetime(string='Hora Salida Sábado')
    
    domingo_labora = fields.Boolean(string='Laborable')
    domingo_entrada = fields.Datetime(string='Hora Entrada Domingo')
    domingo_salida = fields.Datetime(string='Hora Salida Domingo')
