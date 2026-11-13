
{
    'name': 'CTI Core',
    'summary': 'Núcleo central de la plataforma Cyber Threat Intelligence',
    'description': """
        CTI Core proporciona la estructura central de la plataforma:
        - Gestión de entidades e indicadores de compromiso (IoC).
        - Catálogo de fuentes de inteligencia.
        - Trazabilidad y auditoría de operaciones.
        - Control de acceso por roles.
    """,
    'author': 'CTI Platform',
    'category': 'Services/Cybersecurity',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/cti_entity_views.xml',
        'views/cti_source_views.xml',
        'views/cti_audit_log_views.xml',
        'views/cti_menus.xml',
    ],
    'installable': True,
    'application': True,
}
