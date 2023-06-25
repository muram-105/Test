# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class StockLocation(models.Model):
    _inherit = 'stock.location'

    sync = fields.Boolean("Sync")

