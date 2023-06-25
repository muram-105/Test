# -*- coding: utf-8 -*-

from odoo import models, api

class ReportPartnerLedger(models.AbstractModel):
    _inherit = "account.partner.ledger"

    filter_eu_cheques = False

    @api.model
    def _get_options_domain(self, options):
        domain = super(ReportPartnerLedger, self)._get_options_domain(options)
        if options.get('eu_cheques'):
            domain.extend(
               ['|', '|',('payment_id','=',False),
                        ('payment_id.is_cheque','=',False),
                        ('payment_id.cheque_state','in',['collected','refused'])])
        return domain
