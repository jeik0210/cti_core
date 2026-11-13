from odoo import fields, models


class CtiAuditLog(models.Model):
    _name = 'cti.audit.log'
    _description = 'CTI Audit Log'
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Registro', required=True, readonly=True, index=True)
    model_name = fields.Char(string='Modelo', required=True, readonly=True, index=True)
    record_id = fields.Integer(string='ID del registro', required=True, readonly=True, index=True)
    operation = fields.Selection(
        [('create', 'Creación'), ('write', 'Modificación'), ('unlink', 'Eliminación')],
        string='Operación',
        required=True,
        readonly=True,
        index=True,
    )
    user_id = fields.Many2one('res.users', string='Usuario', readonly=True, index=True)
    details = fields.Text(string='Detalle', readonly=True)
