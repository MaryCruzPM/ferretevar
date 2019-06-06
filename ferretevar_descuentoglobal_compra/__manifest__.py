# -*- coding: utf-8 -*-
{
    'name': "Ferretevar descuento global",

    'summary': """add_fields
    """,

    'description': """
        Modulo para hacer descuento global en compra.
    """,

    'author': "Soluciones4G",
    'website': "http://www.soluciones4g.com",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'sale_management',
        'sale',
        'purchase',
        'account',

        ],

	'data': [
   'views/vista_descuento_global.xml',
   'views/reporte_purchase.xml',
   
#    'data/categorias.xml',

    ],
	'demo':[

	],
    'installable':True,
}
