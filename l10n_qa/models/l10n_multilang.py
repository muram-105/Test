# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, models


class AccountChartTemplate(models.Model):
    _inherit = 'account.chart.template'

    def process_coa_translations(self):
        res = super(AccountChartTemplate, self).process_coa_translations()
        if self.id == self.env.ref("l10n_qa.l10nqa_chart_template").id:
            self.env.ref("l10n_me.l10nme_chart_template").process_coa_translations()
        if self.id == self.env.ref("l10n_me.l10nme_chart_template").id:
            installed_langs = dict(self.env['res.lang'].get_installed())
            company_obj = self.env['res.company']
            for chart_template_id in self:
                langs = []
                if chart_template_id.spoken_languages:
                    for lang in chart_template_id.spoken_languages.split(';'):
                        if lang not in installed_langs:
                            # the language is not installed, so we don't need to load its translations
                            continue
                        else:
                            langs.append(lang)
                    if langs:
                        company_ids = company_obj.search([('chart_template_id', '=', self.env.ref("l10n_qa.l10nqa_chart_template").id)])
                        for company in company_ids:
                            # write account.account translations in the real COA
                            chart_template_id._process_accounts_translations(company.id, langs, 'name')
                            # write account.group translations
                            chart_template_id._process_account_group_translations(company.id, langs, 'name')
                            # copy account.tax name translations
                            chart_template_id._process_taxes_translations(company.id, langs, 'name')
                            # copy account.tax description translations
                            chart_template_id._process_taxes_translations(company.id, langs, 'description')
                            # copy account.fiscal.position translations
                            chart_template_id._process_fiscal_pos_translations(company.id, langs, 'name')
        return res


