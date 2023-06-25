# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    name_ar = fields.Char('Name AR', store=False)
    
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        res = super(ProductProduct, self).search_read(domain, fields, offset, limit, order)
        for prod in res:
            product = self.env['product.product'].search([('id','=',prod['id'])])
            prod['name_ar'] = product.with_context(lang='ar_001').name
        return res
    
class POSPM(models.Model):
    _inherit = 'pos.payment.method'
    
    name_ar = fields.Char('Name AR', store=False)
    
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        res = super(POSPM, self).search_read(domain, fields, offset, limit, order)
        for p in res:
            ppm = self.search([('id','=',p['id'])])
            p['name_ar'] = ppm.with_context(lang='ar_001').name
        return res