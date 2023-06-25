# -*- coding: utf-8 -*-

from . import models
from odoo import api, SUPERUSER_ID

def load_translations(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env.ref('l10n_me.l10nme_chart_template').process_coa_translations()
    env.ref('l10n_qa.l10nqa_chart_template').process_coa_translations()
    mods = env['ir.module.module'].search([('state', '=', 'installed')])
    mods.with_context(overwrite=True)._update_translations('ar_001')
