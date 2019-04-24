# -*- coding: utf-8 -*-
{
    'name': "partida odoo11 ventas",

    'summary': """Numero de partida
    """,

    'description': """
        Modulo para ventas de partida automaticamente
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
        'sale',
        'sale_management',
        'venta_cotizacion',
        ],

 #       'purchase',       
 #       'contacts',
 #       'stock',
  

    # always loaded
	'data': [
    
    ],
	'demo':[

	],
    'installable':True,
}
