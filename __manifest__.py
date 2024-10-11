# -*- coding: utf-8 -*-
{
    'name': 'Empleado Horario',
    'version': '1.0',
    'category': 'Human Resources',
    'summary': 'Modulo para registrar empleados y sus horarios laborales.',
    'description': """
        Este módulo permite registrar empleados y sus horarios laborales
        para cada día de la semana.
    """,
    'author': 'Luis Miguel',
    'depends': ['base', 'hr', 'hr_attendance'],
    'data': [
        'views/empleado_views.xml',
        'views/hr_attendance_views.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'application': False,
}
