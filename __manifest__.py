{
    'name': 'CTI Core',
    'summary': 'Catálogo de inteligencia con categorías y subcategorías',
    'description': """
        Organiza las capacidades de inteligencia en categorías y subcategorías,
        y las presenta en un catálogo privado para usuarios del portal.
    """,
    'author': 'CTI Platform',
    'category': 'Services',
    'version': '19.0.3.9.0',
    'license': 'LGPL-3',
    'depends': ['base', 'portal', 'website'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/intelligence_catalog.xml',
        'data/website_menu.xml',
        'views/cti_intelligence_views.xml',
        'views/cti_portal_templates.xml',
        'views/cti_menus.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'cti_core/static/src/js/cti_network_background.js',
            'cti_core/static/src/js/cti_subcategory_workspace.js',
            'cti_core/static/src/scss/cti_portal.scss',
        ],
    },
    'installable': True,
    'application': True,
}
