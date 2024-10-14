from odoo import models, fields

class Branch(models.Model):
    _name = 'hr.branch'
    _description = 'Branch'

    name = fields.Char(string='Sucursal', required=True)