from odoo import fields, models


class CtiIntelligenceCategory(models.Model):
    _name = 'cti.intelligence.category'
    _description = 'Categoría de inteligencia'
    _order = 'sequence, name'

    name = fields.Char(string='Nombre', required=True, translate=True)
    code = fields.Char(string='Código', required=True, index=True)
    icon = fields.Char(string='Icono Font Awesome', default='fa-folder')
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    subcategory_ids = fields.One2many(
        'cti.intelligence.subcategory', 'category_id', string='Subcategorías'
    )

    _sql_constraints = [
        ('cti_intelligence_category_code_unique', 'UNIQUE(code)', 'El código de la categoría debe ser único.'),
    ]


class CtiIntelligenceSubcategory(models.Model):
    _name = 'cti.intelligence.subcategory'
    _description = 'Subcategoría de inteligencia'
    _order = 'sequence, name'

    name = fields.Char(string='Nombre', required=True, translate=True)
    code = fields.Char(string='Código', required=True, index=True)
    category_id = fields.Many2one(
        'cti.intelligence.category',
        string='Categoría',
        required=True,
        ondelete='cascade',
        index=True,
    )
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('cti_intelligence_subcategory_code_unique', 'UNIQUE(code)', 'El código de la subcategoría debe ser único.'),
    ]
