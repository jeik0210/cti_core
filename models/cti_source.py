
from odoo import api, fields, models


class CtiSource(models.Model):
    _name = 'cti.source'
    _description = 'CTI Intelligence Source'
    _order = 'name'

    name = fields.Char(
        string='Nombre de la fuente',
        required=True,
        index=True,
    )

    code = fields.Char(
        string='Código',
        required=True,
        index=True,
        copy=False,
    )

    source_type = fields.Selection(
        selection=[
            ('osint', 'OSINT'),
            ('commercial', 'Comercial'),
            ('internal', 'Interna'),
            ('community', 'Comunitaria'),
            ('government', 'Gubernamental'),
            ('other', 'Otra'),
        ],
        string='Tipo de fuente',
        required=True,
        default='osint',
    )

    website_url = fields.Char(
        string='URL de referencia',
    )

    reliability = fields.Selection(
        selection=[
            ('a', 'A - Muy confiable'),
            ('b', 'B - Confiable'),
            ('c', 'C - Moderadamente confiable'),
            ('d', 'D - Poco confiable'),
            ('e', 'E - No confiable'),
            ('f', 'F - Sin información'),
        ],
        string='Confiabilidad',
        default='f',
        required=True,
    )

    description = fields.Text(
        string='Descripción',
    )

    last_verified = fields.Datetime(
        string='Última verificación',
    )

    active = fields.Boolean(
        string='Activo',
        default=True,
    )

    _sql_constraints = [
        (
            'cti_source_code_unique',
            'UNIQUE(code)',
            'El código de la fuente debe ser único.',
        ),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            record._log_cti_event('create', 'Fuente creada.')
        return records

    def write(self, vals):
        result = super().write(vals)
        if vals:
            changed_fields = ', '.join(sorted(vals))
            for record in self:
                record._log_cti_event('write', 'Campos modificados: %s' % changed_fields)
        return result

    def unlink(self):
        for record in self:
            record._log_cti_event('unlink', 'Fuente eliminada.')
        return super().unlink()

    def _log_cti_event(self, operation, details):
        self.env['cti.audit.log'].sudo().create({
            'name': self.name,
            'model_name': self._name,
            'record_id': self.id,
            'operation': operation,
            'user_id': self.env.user.id,
            'details': details,
        })
