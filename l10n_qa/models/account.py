# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class Company(models.Model):
    _inherit = "res.company"
    
    def _init_column(self, column_name):
        res = super(Company, self)._init_column(column_name)
        if "account_tax_periodicity" ==  column_name:
            for company in self.env['res.company'].search([]).filtered(lambda x:x.chart_template_id.id == self.env.ref("l10n_qa.l10nqa_chart_template").id):
                company.account_tax_periodicity = "trimester"
        return res
     
class AccountChartTemplate(models.Model):
    _inherit = "account.chart.template"
    
    def _load(self, company):
        res = super(AccountChartTemplate, self)._load(company)
        if self.id == self.env.ref("l10n_qa.l10nqa_chart_template").id:
            sales_vat = self.env.ref("l10n_me.%s_account_account_template_sale"%(company.id))
            sales_vat.name = 'Sales VAT Deposits'
            purchase_vat = self.env.ref("l10n_me.%s_account_account_template_purchase_dep"%(company.id))
            purchase_vat.name = "Purchase VAT Deposit"
            rounded_vat = self.env.ref("l10n_me.%s_account_account_template_rounded_dep"%(company.id))
            rounded_vat.name = "Rounded VAT Deposits"
            rounded_vat = self.env.ref("l10n_me.%s_account_account_template_inc"%(company.id))
            rounded_vat.name = "General Tax Authority"
            
            tax_group1 = self.env.ref('l10n_qa.tax_group_basic', False)
            tax_group1.write(
                {'property_tax_payable_account_id': self.env.ref('l10n_me.account_account_template_inc').id,
                 'property_tax_receivable_account_id': self.env.ref('l10n_me.account_account_template_rounded_dep').id})
            tax_group2 = self.env.ref('l10n_qa.tax_group_local_sale', False)
            tax_group2.write(
                {'property_tax_payable_account_id': self.env.ref('l10n_me.account_account_template_inc').id,
                 'property_tax_receivable_account_id': self.env.ref('l10n_me.account_account_template_rounded_dep').id})
            tax_group3 = self.env.ref('l10n_qa.tax_group_export_sale', False)
            tax_group3.write(
                {'property_tax_payable_account_id': self.env.ref('l10n_me.account_account_template_inc').id,
                 'property_tax_receivable_account_id': self.env.ref('l10n_me.account_account_template_rounded_dep').id})
            tax_group4 = self.env.ref('l10n_qa.tax_group_non_taxable_sales', False)
            tax_group4.write(
                {'property_tax_payable_account_id': self.env.ref('l10n_me.account_account_template_inc').id,
                 'property_tax_receivable_account_id': self.env.ref('l10n_me.account_account_template_rounded_dep').id})
            tax_group5 = self.env.ref('l10n_qa.tax_group_nonrefundable', False)
            tax_group5.write(
                {'property_tax_payable_account_id': self.env.ref('l10n_me.account_account_template_inc').id,
                 'property_tax_receivable_account_id': self.env.ref('l10n_me.account_account_template_rounded_dep').id})
            tax_group6 = self.env.ref('l10n_qa.tax_group_vat_adjusment', False)
            tax_group6.write(
                {'property_tax_payable_account_id': self.env.ref('l10n_me.account_account_template_inc').id,
                 'property_tax_receivable_account_id': self.env.ref('l10n_me.account_account_template_rounded_dep').id})
            tax_group7 = self.env.ref('l10n_qa.tax_group_import', False)
            tax_group7.write(
                {'property_tax_payable_account_id': self.env.ref('l10n_me.account_account_template_inc').id,
                 'property_tax_receivable_account_id': self.env.ref('l10n_me.account_account_template_rounded_dep').id})
            tax_group8 = self.env.ref('l10n_qa.tax_group_import_vat', False)
            tax_group8.write(
                {'property_tax_payable_account_id': self.env.ref('l10n_me.account_account_template_inc').id,
                 'property_tax_receivable_account_id': self.env.ref('l10n_me.account_account_template_rounded_dep').id}) 
            tax_group9 = self.env.ref('l10n_qa.tax_group_import_deffered', False)
            tax_group9.write(
                {'property_tax_payable_account_id': self.env.ref('l10n_me.account_account_template_inc').id,
                 'property_tax_receivable_account_id': self.env.ref('l10n_me.account_account_template_rounded_dep').id})
            tax_group10 = self.env.ref('l10n_qa.tax_group_p0', False)
            tax_group10.write(
                {'property_tax_payable_account_id': self.env.ref('l10n_me.account_account_template_inc').id,
                 'property_tax_receivable_account_id': self.env.ref('l10n_me.account_account_template_rounded_dep').id})
            tax_group11 = self.env.ref('l10n_qa.tax_group_citizens', False)
            tax_group11.write(
                {'property_tax_payable_account_id': self.env.ref('l10n_me.account_account_template_inc').id,
                 'property_tax_receivable_account_id': self.env.ref('l10n_me.account_account_template_rounded_dep').id})
            tax_group12 = self.env.ref('l10n_qa.tax_group_pe', False)
            tax_group12.write(
                {'property_tax_payable_account_id': self.env.ref('l10n_me.account_account_template_inc').id,
                 'property_tax_receivable_account_id': self.env.ref('l10n_me.account_account_template_rounded_dep').id})
            tax_group13 = self.env.ref('l10n_qa.tax_group_se', False)
            tax_group13.write(
                {'property_tax_payable_account_id': self.env.ref('l10n_me.account_account_template_inc').id,
                 'property_tax_receivable_account_id': self.env.ref('l10n_me.account_account_template_rounded_dep').id})
        if self.id == self.env.ref("l10n_qa.l10nqa_chart_template").id:
            if hasattr(company, 'account_tax_periodicity'):
                company.account_tax_periodicity = "trimester"
        return res
    

    def generate_account_reconcile_model(self, tax_template_ref, acc_template_ref, company):
        if self.id == self.env.ref("l10n_qa.l10nqa_chart_template").id:
            return True
        else:
             return super(AccountChartTemplate, self).generate_account_reconcile_model(tax_template_ref, acc_template_ref, company)