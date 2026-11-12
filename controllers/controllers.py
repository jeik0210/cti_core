# from odoo import http


# class CtiCore(http.Controller):
#     @http.route('/cti_core/cti_core', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cti_core/cti_core/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('cti_core.listing', {
#             'root': '/cti_core/cti_core',
#             'objects': http.request.env['cti_core.cti_core'].search([]),
#         })

#     @http.route('/cti_core/cti_core/objects/<model("cti_core.cti_core"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cti_core.object', {
#             'object': obj
#         })

