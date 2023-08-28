# -*- coding: utf-8 -*-
{
    'name': "Riders",

    'summary': """
       Gestion de Riders para empresas de transporte minoristas.""",

    'description': """
        Este módulo permite una gestión adecuada de las ordenes, riders y rutas. Esta orientado a apps de transportes
        u otras empresas que quieran implementar el servicio de entrega a traves de riders.
    """,

    'author': "Big_Al",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Service',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    # Indicamos que es una aplicacion
    'application': True,
}
