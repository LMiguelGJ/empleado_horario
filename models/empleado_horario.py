# -*- coding: utf-8 -*-
from odoo import models, fields

class Employee(models.Model):
    _inherit = 'hr.employee'
    
    branch_id = fields.Many2one('hr.branch', string='Sucursal', required=False, ondelete='set null', help='Sucursal a la que pertenece el empleado', index=True)

    HOURS_SELECTION = [
        ('4', '4 Horas'),
        ('5', '5 Horas'),
        ('6', '6 Horas'),
        ('7', '7 Horas'),
        ('8', '8 Horas'),
        ('9', '9 Horas'),
    ]

    monday_hours = fields.Selection(HOURS_SELECTION, string="Monday Hours", default='8')
    tuesday_hours = fields.Selection(HOURS_SELECTION, string="Tuesday Hours", default='8')
    wednesday_hours = fields.Selection(HOURS_SELECTION, string="Wednesday Hours", default='8')
    thursday_hours = fields.Selection(HOURS_SELECTION, string="Thursday Hours", default='8')
    friday_hours = fields.Selection(HOURS_SELECTION, string="Friday Hours", default='8')
    saturday_hours = fields.Selection(HOURS_SELECTION, string="Saturday Hours", default='4')
    sunday_hours = fields.Selection(HOURS_SELECTION, string="Sunday Hours")