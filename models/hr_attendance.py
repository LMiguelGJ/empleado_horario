from odoo import models, fields, api
from datetime import datetime


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    date_in = fields.Date(string="Fecha de Ingreso")
    extra_hours = fields.Float(string="Horas Extra", compute="_compute_extra_hours", store=True)
    branch_id = fields.Many2one(
        'hr.branch',  
        string="Sucursal",  
        related='employee_id.branch_id', 
        store=True  
    )
    
    department_id = fields.Many2one(
        'hr.department', 
        string="Departamento", 
        related='employee_id.department_id', 
        store=True
    )

    check_in_12h = fields.Char(
        string="Entrada", 
        compute="_compute_12h_format", 
        store=True
    )
    check_out_12h = fields.Char(
        string="Salida", 
        compute="_compute_12h_format", 
        store=True
    )

    @api.depends('check_in', 'check_out')
    def _compute_12h_format(self):
        for record in self:
            if record.check_in:
                record.check_in_12h = datetime.strftime(
                    fields.Datetime.to_datetime(record.check_in), "%I:%M %p"
                )
            else:
                record.check_in_12h = ''
            if record.check_out:
                record.check_out_12h = datetime.strftime(
                    fields.Datetime.to_datetime(record.check_out), "%I:%M %p"
                )
            else:
                record.check_out_12h = ''


    @api.depends('worked_hours', 'employee_id')
    def _compute_extra_hours(self):
        for record in self:
            if record.employee_id:
                # Obtén el día de la semana del registro
                day_of_week = record.check_in.weekday()  # 0=Monday, 1=Tuesday, ..., 6=Sunday
                
                # Obtén las horas programadas del empleado
                hours_planned = 0
                if record.employee_id:
                    # Asumiendo que tienes un método que obtiene las horas programadas del día
                    if day_of_week == 0:  # Lunes
                        hours_planned = record.employee_id.monday_hours
                    elif day_of_week == 1:  # Martes
                        hours_planned = record.employee_id.tuesday_hours
                    elif day_of_week == 2:  # Miércoles
                        hours_planned = record.employee_id.wednesday_hours
                    elif day_of_week == 3:  # Jueves
                        hours_planned = record.employee_id.thursday_hours
                    elif day_of_week == 4:  # Viernes
                        hours_planned = record.employee_id.friday_hours
                    elif day_of_week == 5:  # Sábado
                        hours_planned = record.employee_id.saturday_hours
                    elif day_of_week == 6:  # Domingo
                        hours_planned = record.employee_id.sunday_hours

                # Calcula las horas extra
                hours_planned = float(hours_planned) if hours_planned else 0
                if record.worked_hours > hours_planned:
                    record.extra_hours = record.worked_hours - hours_planned
                else:
                    record.extra_hours = 0.0
