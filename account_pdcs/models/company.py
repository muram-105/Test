# -*- coding: utf-8 -*-

from odoo import models, fields

class Company(models.Model):
    _inherit = "res.company"

    account_check_printing_layout = fields.Selection(selection_add=[
        ('account_pdcs.action_print_check_jo', 'Print Check Jordan'),
    ], ondelete={
        'account_pdcs.action_print_check_jo': 'set default',
    })
