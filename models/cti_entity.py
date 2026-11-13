from odoo import api, fields, models
from odoo.exceptions import ValidationError


class CtiEntity(models.Model):
    _name = 'cti.entity'
    _description = 'CTI Entity / Indicator of Compromise'
    _order = 'last_seen desc, name'

    name = fields.Char(string='Nombre', required=True, index=True)
    entity_type = fields.Selection(
        [
            ('ip', 'Dirección IP'),
            ('domain', 'Dominio'),
            ('url', 'URL'),
            ('email', 'Correo electrónico'),
            ('file_hash', 'Hash de archivo'),
            ('file_name', 'Nombre de archivo'),
            ('organization', 'Organización'),
            ('person', 'Persona'),
            ('other', 'Otro'),
        ],
        string='Tipo',
        required=True,
        index=True,
    )
    value = fields.Char(string='Valor observable', required=True, index=True)
    state = fields.Selection(
        [('new', 'Nuevo'), ('investigating', 'En investigación'), ('confirmed', 'Confirmado'), ('false_positive', 'Falso positivo'), ('expired', 'Expirado')],
        string='Estado',
        required=True,
        default='new',
        index=True,
    )
    severity = fields.Selection(
        [('low', 'Baja'), ('medium', 'Media'), ('high', 'Alta'), ('critical', 'Crítica')],
        string='Severidad',
        required=True,
        default='medium',
        index=True,
    )
    confidence = fields.Integer(string='Confianza (%)', default=50)
    source_ids = fields.Many2many(
        'cti.source',
        'cti_entity_source_rel',
        'entity_id',
        'source_id',
        string='Fuentes',
    )
    first_seen = fields.Datetime(string='Primera detección', default=fields.Datetime.now)
    last_seen = fields.Datetime(string='Última detección', default=fields.Datetime.now)
    description = fields.Text(string='Descripción / contexto')
    active = fields.Boolean(default=True)

    @api.constrains('confidence')
    def _check_confidence(self):
        for record in self:
            if not 0 <= record.confidence <= 100:
                raise ValidationError('La confianza debe estar entre 0 y 100.')

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            record._log_cti_event('create', 'Registro creado.')
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
            record._log_cti_event('unlink', 'Registro eliminado.')
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
