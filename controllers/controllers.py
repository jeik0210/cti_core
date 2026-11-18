from odoo import http
from odoo.http import request


class CtiPortalController(http.Controller):

    @http.route(
        '/portal',
        type='http',
        auth='public',
        website=True,
        sitemap=True,
        list_as_website_content='Portal de consultas',
        readonly=True,
    )
    def public_landing(self, **kwargs):
        return request.render('cti_core.portal_landing', {
            'is_public': request.env.user._is_public(),
        })

    @http.route(
        '/my/consultas',
        type='http',
        auth='user',
        website=True,
        readonly=True,
        sitemap=False,
    )
    def portal_intelligence_catalog(self, **kwargs):
        categories = request.env['cti.intelligence.category'].sudo().search(
            [('active', '=', True)], order='sequence, name'
        )
        catalog = []
        for category in categories:
            subcategories = request.env['cti.intelligence.subcategory'].sudo().search(
                [('category_id', '=', category.id), ('active', '=', True)],
                order='sequence, name',
            )
            catalog.append({
                'category': category,
                'subcategories': subcategories,
            })
        return request.render('cti_core.portal_query_services', {'catalog': catalog})

    @http.route(
        '/my/consultas/<string:code>',
        type='http',
        auth='user',
        website=True,
        readonly=True,
        sitemap=False,
    )
    def portal_intelligence_subcategory(self, code, **kwargs):
        subcategory = request.env['cti.intelligence.subcategory'].sudo().search(
            [
                ('code', '=', code),
                ('active', '=', True),
                ('category_id.active', '=', True),
            ],
            limit=1,
        )
        if not subcategory:
            return request.not_found()
        return request.render('cti_core.portal_intelligence_subcategory', {
            'subcategory': subcategory,
            'category': subcategory.category_id,
        })
