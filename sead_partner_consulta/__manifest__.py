# -*- coding: utf-8 -*-

{
    'name': 'Sead Partner Consulta RUC y DNI',
    'version': '13.0.1.0.0',
    'author': 'SEAD SAC',
    'website': 'http://www.sead.pe',
    'summary': 'Integracion con APIsPERU',
    'description': """ Este módulo se integra con APIsPERU para realizar consultas de RUC y DNI
                        """,
    'depends': [
        'base',
    ],
    'data': [
        
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'auto_install': False
}

