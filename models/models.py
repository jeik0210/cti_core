# from odoo import models, fields, api


# class cti_core(models.Model):
#     _name = 'cti_core.cti_core'
#     _description = 'cti_core.cti_core'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

