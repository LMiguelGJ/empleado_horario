# -*- coding: utf-8 -*-
{
    'name': 'Empleado Horario',
    'version': '1.0',
    'sequence': -1,
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
        'wizards/import_attendance_wizard_view.xml',
        'security/ir.model.access.csv'
    ],
    'assets': {
        'web.assets_backend': [
            'empleado_horario/static/src/components/*'
        ]
    },
    'installable': True,
    'application': True,
    
    }
