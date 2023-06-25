# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class AccountAsset(models.Model):
    _inherit = "account.asset"
    
    name = fields.Char(string='Asset Name', compute='_compute_name', store=True, required=True, readonly=False, tracking=True, translate=True)
    
    @api.depends('company_id')
    def _compute_journal_id(self):
        for asset in self:
            if not asset.journal_id:
                asset.journal_id = self.env['account.journal'].search([('type', '=', 'general'), ('company_id', '=', asset.company_id.id)], limit=1)
            else:
                asset.journal_id = asset.journal_id.id

class AccountChartTemplate(models.Model):
    _inherit = "account.chart.template"
    
    def load_account_assets(self,company):
        env = self.env
        asset_model = env["account.asset"]
        er_journal = env["account.journal"].search([('type','=','general'),('code','=','ER'),('company_id','=',company.id)],limit=1)
        sale_journal = env["account.journal"].search([('type','=','sale'),('code','=','INV'),('company_id','=',company.id)])
        purchase_journal = env["account.journal"].search([('type','=','purchase'),('code','=','BILL'),('company_id','=',company.id)])
        rr_journal = env["account.journal"].search([('type','=','general'),('code','=','RR'),('company_id','=',company.id)],limit=1)
        rent_account = env.ref("l10n_me.%s_account_account_template_56"%(company.id), False)
        prepaid_rent_account = env.ref("l10n_me.%s_account_account_template_12"%(company.id), False)
        internet_account = env.ref("l10n_me.%s_account_account_template_71"%(company.id), False)
        prepaid_internet_account = env.ref("l10n_me.%s_account_account_template_11"%(company.id), False)
        prepaid_main = env.ref("l10n_me.%s_account_account_template_10"%(company.id), False)
        maint_account = env.ref("l10n_me.%s_account_account_template_59"%(company.id), False)
        prepaid_h_ins = env.ref("l10n_me.%s_account_account_template_13"%(company.id), False)
        health_insurance_exp_acc = env.ref("l10n_me.%s_account_account_template_122"%(company.id), False)
        ur_12_acc = self.env.ref("l10n_me.%s_account_account_template_36"%(company.id), False)
        ur_6_acc = self.env.ref("l10n_me.%s_account_account_template_111"%(company.id), False)
        ur_3_acc = self.env.ref("l10n_me.%s_account_account_template_112"%(company.id), False)
        ur_2_acc = self.env.ref("l10n_me.%s_account_account_template_113"%(company.id), False)
        ur_1_acc = self.env.ref("l10n_me.%s_account_account_template_114"%(company.id), False)
        sales_acc = self.env.ref("l10n_me.%s_account_account_template_50"%(company.id), False)
        
        if ur_12_acc and sales_acc:
            asset_9 = asset_model.create({
                "name":"Unearned Revenues 12M",
                "method_period":'1',
                "method_number":12,
                "journal_id":rr_journal.id,
                "asset_type":'sale',
                'prorata_computation_type': 'constant_periods',
                "account_depreciation_id":ur_12_acc.id,
                "account_depreciation_expense_id":sales_acc.id,
                "state":"model"
                })
            asset_9._update_field_translations('name', {'ar_001': 'ايرادات غير مكتسبة 12 شهر'})
            
            if ur_12_acc:
                ur_12_acc.create_asset = 'draft'
                ur_12_acc.asset_model = asset_9.id
                
        if ur_6_acc and sales_acc:
            asset_10 = asset_model.create({
                "name":"Unearned Revenues 6M",
                "method_period":'1',
                "method_number":6,
                "journal_id":rr_journal.id,
                "asset_type":'sale',
                'prorata_computation_type': 'constant_periods',
                "account_depreciation_id":ur_6_acc.id,
                "account_depreciation_expense_id":sales_acc.id,
                "state":"model"
                })
            asset_10._update_field_translations('name', {'ar_001': 'ايرادات غير مكتسبة 6 شهر'})
            
            if ur_6_acc:
                ur_6_acc.create_asset = 'draft'
                ur_6_acc.asset_model = asset_10.id
            
        if ur_3_acc and sales_acc:
            asset_11 = asset_model.create({
                "name":"Unearned Revenues 3M",
                "method_period":'1',
                "method_number":3,
                "journal_id":rr_journal.id,
                "asset_type":'sale',
                'prorata_computation_type': 'constant_periods',
                "account_depreciation_id":ur_3_acc.id,
                "account_depreciation_expense_id":sales_acc.id,
                "state":"model"
                })
            asset_11._update_field_translations('name', {'ar_001': 'ايرادات غير مكتسبة 3 شهر'})
            
            if ur_3_acc:
                ur_3_acc.create_asset = 'draft'
                ur_3_acc.asset_model = asset_11.id
            
        if ur_2_acc and sales_acc:
            asset_12 = asset_model.create({
                "name":"Unearned Revenues 2M",
                "method_period":'1',
                "method_number":2,
                "journal_id":rr_journal.id,
                "asset_type":'sale',
                'prorata_computation_type': 'constant_periods',
                "account_depreciation_id":ur_2_acc.id,
                "account_depreciation_expense_id":sales_acc.id,
                "state":"model"
                })
            asset_12._update_field_translations('name', {'ar_001': 'ايرادات غير مكتسبة 2 شهر'})
            
            if ur_2_acc:
                ur_2_acc.create_asset = 'draft'
                ur_2_acc.asset_model = asset_12.id
            
        if ur_1_acc and sales_acc:
            asset_13 = asset_model.create({
                "name":"Unearned Revenues 1M",
                "method_period":'1',
                "method_number":1,
                "journal_id":rr_journal.id,
                "asset_type":'sale',
                'prorata_computation_type': 'constant_periods',
                "account_depreciation_id":ur_1_acc.id,
                "account_depreciation_expense_id":sales_acc.id,
                "state":"model"
                })
            asset_13._update_field_translations('name', {'ar_001': 'ايرادات غير مكتسبة 1 شهر'})
            
            if ur_1_acc:
                ur_1_acc.create_asset = 'draft'
                ur_1_acc.asset_model = asset_13.id
        
        if maint_account and prepaid_main:
            asset_7 = asset_model.create({
                "name":"12M - Maintenance",
                "method_period":'1',
                "method_number":12,
                "journal_id":er_journal.id,
                "asset_type":'expense',
                'prorata_computation_type': 'constant_periods',
                "account_depreciation_id":prepaid_main.id,
                "account_depreciation_expense_id":maint_account.id,
                "state":"model"
                })
            asset_7._update_field_translations('name', {'ar_001': 'صيانة'})
            
        if prepaid_h_ins and health_insurance_exp_acc:
            asset_8 = asset_model.create({
                "name":"12M - Health Insurance",
                "method_period":'1',
                "method_number":12,
                "journal_id":er_journal.id,
                "asset_type":'expense',
                'prorata_computation_type': 'constant_periods',
                "account_depreciation_id":prepaid_h_ins.id,
                "account_depreciation_expense_id":health_insurance_exp_acc.id,
                "state":"model"
                })
            asset_8._update_field_translations('name', {'ar_001': 'تامين صحي'})
        
        if prepaid_rent_account and rent_account:
            asset_1 = asset_model.create({
                "name":"12M - Rent",
                "method_period":'1',
                "method_number":12,
                "journal_id":er_journal.id,
                "asset_type":'expense',
                'prorata_computation_type': 'constant_periods',
                "account_depreciation_id":prepaid_rent_account.id,
                "account_depreciation_expense_id":rent_account.id,
                "state":"model"
                })
            asset_1._update_field_translations('name', {'ar_001': 'عام واحد - ايجارات'})
            
        if prepaid_internet_account and internet_account:
            asset_2 = asset_model.create({
                "name":"12M - Internet",
                "method_period":'1',
                "method_number":12,
                "journal_id":er_journal.id,
                "asset_type":'expense',
                'prorata_computation_type': 'constant_periods',
                "account_depreciation_id":prepaid_internet_account.id,
                "account_depreciation_expense_id":internet_account.id,
                "state":"model"
                })
            asset_2._update_field_translations('name', {'ar_001': 'عام واحد - انترنت'})
            
        if prepaid_rent_account and rent_account:
            asset_3 = asset_model.create({
                "name":"6M - Rent",
                "method_period":'1',
                "method_number":6,
                "journal_id":er_journal.id,
                "asset_type":'expense',
                'prorata_computation_type': 'constant_periods',
                "account_depreciation_id":prepaid_rent_account.id,
                "account_depreciation_expense_id":rent_account.id,
                "state":"model"
                })
            asset_3._update_field_translations('name', {'ar_001': 'ستة اشهر - ايجارات'})
        
        if prepaid_internet_account and internet_account:
            asset_4 = asset_model.create({
                "name":"6M - Internet",
                "method_period":'1',
                "method_number":6,
                "journal_id":er_journal.id,
                "asset_type":'expense',
                'prorata_computation_type': 'constant_periods',
                "account_depreciation_id":prepaid_internet_account.id,
                "account_depreciation_expense_id":internet_account.id,
                "state":"model"
                })
            asset_4._update_field_translations('name', {'ar_001': 'ستة اشهر - انترنت'})
            
        if prepaid_rent_account and rent_account:
            asset_5 = asset_model.create({
                "name":"3M - Rent",
                "method_period":'1',
                "method_number":3,
                "journal_id":er_journal.id,
                "asset_type":'expense',
                'prorata_computation_type': 'constant_periods',
                "account_depreciation_id":prepaid_rent_account.id,
                "account_depreciation_expense_id":rent_account.id,
                "state":"model"
                })
            asset_5._update_field_translations('name', {'ar_001': 'ثلاثة اشهر - ايجارات'})
        
        if prepaid_internet_account and internet_account:
            asset_6 = asset_model.create({
                "name":"3M - Internet",
                "method_period":'1',
                "method_number":3,
                "journal_id":er_journal.id,
                "asset_type":'expense',
                'prorata_computation_type': 'constant_periods',
                "account_depreciation_id":prepaid_internet_account.id,
                "account_depreciation_expense_id":internet_account.id,
                "state":"model"
                })
            asset_6._update_field_translations('name', {'ar_001': 'ثلاثة اشهر - انترنت'})
        
        fa_journal = self.env["account.journal"].search([('company_id','=',company.id),('code','=',"FA")],limit=1)
        if not fa_journal:
            fa_journal = env["account.journal"].create({
                "name":"Fixed Assets",
                "code":"FA",
                "type":"general",
                'show_on_dashboard':False,
                "company_id":company.id,
                })
            fa_journal._update_field_translations('name', {'ar_001': 'الأصول الثابتة'})
        
        tools_and_eq_acc = env.ref("l10n_me.%s_account_account_template_25"%(company.id), False)
        tools_and_eq_dep_acc = env.ref("l10n_me.%s_account_account_template_26"%(company.id), False)
        tools_and_eq_exp_acc = env.ref("l10n_me.%s_account_account_template_82"%(company.id), False)
        if tools_and_eq_acc and tools_and_eq_dep_acc and tools_and_eq_exp_acc:
            tools_and_eq = asset_model.create({
                "name":_("Tools and Equipments"),
                "asset_type":"purchase",
                'prorata_computation_type': 'constant_periods',
                "state":"model",
                "method":"linear",
                "method_number":60,
                "method_period":"1",
                "journal_id":fa_journal.id,
                "account_asset_id":tools_and_eq_acc.id,
                "account_depreciation_id":tools_and_eq_dep_acc.id,
                "account_depreciation_expense_id":tools_and_eq_exp_acc.id,
                "company_id":company.id
                })
            tools_and_eq._update_field_translations('name', {'ar_001': 'عدد و معدات'})
            
            tools_and_eq_acc.create_asset = "draft"
            tools_and_eq_acc.multiple_assets_per_line = False
            tools_and_eq_acc.asset_model = tools_and_eq.id  
            tools_and_eq_acc.allowed_journal_ids = [(6,0,[sale_journal.id,purchase_journal.id])]
            tools_and_eq_exp_acc.allowed_journal_ids = [(6,0,[fa_journal.id])]
        
        elect_acc = env.ref("l10n_me.%s_account_account_template_98"%(company.id), False)
        elect_dep_acc = env.ref("l10n_me.%s_account_account_template_97"%(company.id), False)
        elect_exp_acc = env.ref("l10n_me.%s_account_account_template_99"%(company.id), False)
        
        if  elect_acc and elect_dep_acc and elect_exp_acc:
            elect = asset_model.create({
                "name":_("Electricity Devices"),
                "asset_type":"purchase",
                'prorata_computation_type': 'constant_periods',
                "state":"model",
                "method":"linear",
                 "method_number":36,
                 "method_period":"1",
                "journal_id":fa_journal.id,
                "account_asset_id":elect_acc.id,
                "account_depreciation_id":elect_dep_acc.id,
                "account_depreciation_expense_id":elect_exp_acc.id,
                 "company_id":company.id
                })
            elect._update_field_translations('name', {'ar_001': 'اجهزة الكترونية'})
            
            elect_acc.create_asset = "draft"
            elect_acc.multiple_assets_per_line = False
            elect_acc.asset_model = elect.id  
            elect_acc.allowed_journal_ids = [(6,0,[sale_journal.id,purchase_journal.id])]
            elect_exp_acc.allowed_journal_ids = [(6,0,[fa_journal.id])]
        
        furniture_acc = env.ref("l10n_me.%s_account_account_template_15"%(company.id), False)
        furniture_dep_acc = env.ref("l10n_me.%s_account_account_template_16"%(company.id), False)
        furniture_exp_acc = env.ref("l10n_me.%s_account_account_template_78"%(company.id), False)
        
        if furniture_acc and furniture_dep_acc and furniture_exp_acc:
            furniture = asset_model.create({
                "name":_("Furniture"),
                "asset_type":"purchase",
                'prorata_computation_type': 'constant_periods',
                "state":"model",
                "method":"linear",
                 "method_number":60,
                 "method_period":"1",
                "journal_id":fa_journal.id,
                "account_asset_id":furniture_acc.id,
                "account_depreciation_id":furniture_dep_acc.id,
                "account_depreciation_expense_id":furniture_exp_acc.id,
                 "company_id":company.id
                })
            furniture._update_field_translations('name', {'ar_001': 'اثاث'})
        
            furniture_acc.create_asset = "draft"
            furniture_acc.multiple_assets_per_line = False
            furniture_acc.asset_model = furniture.id  
            furniture_exp_acc.allowed_journal_ids = [(6, 0, [fa_journal.id])]
        
        decoration_acc = env.ref("l10n_me.%s_account_account_template_21"%(company.id), False)
        decoration_dep_acc = env.ref("l10n_me.%s_account_account_template_22"%(company.id), False)
        decoration_exp_acc = env.ref("l10n_me.%s_account_account_template_81"%(company.id), False)
        
        if decoration_acc and decoration_dep_acc and decoration_exp_acc:
            decoration = asset_model.create({
                "name":_("Decorations"),
                "asset_type":"purchase",
                'prorata_computation_type': 'constant_periods',
                "state":"model",
                "method":"linear",
                 "method_number":120,
                 "method_period":"1",
                "journal_id":fa_journal.id,
                "account_asset_id":decoration_acc.id,
                "account_depreciation_id":decoration_dep_acc.id,
                "account_depreciation_expense_id":decoration_exp_acc.id,
                 "company_id":company.id
                })
            decoration._update_field_translations('name', {'ar_001': 'الديكورات'})
            
            decoration_acc.create_asset = "draft"
            decoration_acc.multiple_assets_per_line = False
            decoration_acc.asset_model = decoration.id  
            decoration_acc.allowed_journal_ids = [(6,0,[sale_journal.id,purchase_journal.id])]
            decoration_exp_acc.allowed_journal_ids = [(6,0,[fa_journal.id])]

        computers_acc = env.ref("l10n_me.%s_account_account_template_17"%(company.id), False)
        computers_dep_acc = env.ref("l10n_me.%s_account_account_template_18"%(company.id), False)
        computers_exp_acc = env.ref("l10n_me.%s_account_account_template_79"%(company.id), False)
        
        if computers_acc and computers_dep_acc and computers_exp_acc:
            computer = asset_model.create({
                "name":_("Computers"),
                "asset_type":"purchase",
                'prorata_computation_type': 'constant_periods',
                "state":"model",
                "method":"linear",
                 "method_number":34,
                 "method_period":"1",
                "journal_id":fa_journal.id,
                "account_asset_id":computers_acc.id,
                "account_depreciation_id":computers_dep_acc.id,
                "account_depreciation_expense_id":computers_exp_acc.id,
                 "company_id":company.id
                })
            computer._update_field_translations('name', {'ar_001': 'الحاسبات'})
            
            computers_acc.create_asset = "draft"
            computers_acc.multiple_assets_per_line = True
            computers_acc.asset_model = computer.id  
            computers_acc.allowed_journal_ids = [(6,0,[sale_journal.id,purchase_journal.id])]
            computers_exp_acc.allowed_journal_ids = [(6,0,[fa_journal.id])]
        
        car_acc = env.ref("l10n_me.%s_account_account_template_23"%(company.id), False)
        car_dep_acc = env.ref("l10n_me.%s_account_account_template_24"%(company.id), False)
        car_exp_acc = env.ref("l10n_me.%s_account_account_template_77"%(company.id), False)
        
        if car_acc and car_dep_acc and car_exp_acc:
            car = asset_model.create({
                "name":_("Cars"),
                "asset_type":"purchase",
                'prorata_computation_type': 'constant_periods',
                "state":"model",
                "method":"linear",
                 "method_number":80,
                 "method_period":"1",
                "journal_id":fa_journal.id,
                "account_asset_id":car_acc.id,
                "account_depreciation_id":car_dep_acc.id,
                "account_depreciation_expense_id":car_exp_acc.id,
                 "company_id":company.id
                })
            car._update_field_translations('name', {'ar_001': 'السيارات'})
            
            car_acc.create_asset = "draft"
            car_acc.multiple_assets_per_line = False
            car_acc.asset_model = car.id  
            car_acc.allowed_journal_ids = [(6,0,[sale_journal.id,purchase_journal.id])]
            car_exp_acc.allowed_journal_ids = [(6,0,[fa_journal.id])]
        
        conditions_acc = env.ref("l10n_me.%s_account_account_template_19"%(company.id), False)
        conditions_dep_acc = env.ref("l10n_me.%s_account_account_template_20"%(company.id), False)
        conditions_exp_acc = env.ref("l10n_me.%s_account_account_template_80"%(company.id), False)
        
        if conditions_acc and conditions_dep_acc and conditions_exp_acc:
            conditions = asset_model.create({
                "name":_("Air Conditions"),
                "asset_type":"purchase",
                'prorata_computation_type': 'constant_periods',
                "state":"model",
                "method":"linear",
                 "method_number":24,
                 "method_period":"1",
                "journal_id":fa_journal.id,
                "account_asset_id":conditions_acc.id,
                "account_depreciation_id":conditions_dep_acc.id,
                "account_depreciation_expense_id":conditions_exp_acc.id,
                 "company_id":company.id
                })
            conditions._update_field_translations('name', {'ar_001': 'المكيفات'})
            
            conditions_acc.create_asset = "draft"
            conditions_acc.multiple_assets_per_line = False
            conditions_acc.asset_model = conditions.id  
            conditions_acc.allowed_journal_ids = [(6,0,[sale_journal.id,purchase_journal.id])]
            conditions_exp_acc.allowed_journal_ids = [(6,0,[fa_journal.id])]
        
        acc_sys_acc = env.ref("l10n_me.%s_account_account_template_27"%(company.id), False)
        acc_sys_dep_acc = env.ref("l10n_me.%s_account_account_template_28"%(company.id), False)
        acc_sys_exp_acc = env.ref("l10n_me.%s_account_account_template_83"%(company.id), False)
        
        if acc_sys_acc and acc_sys_dep_acc and acc_sys_exp_acc:
            acc_sys = asset_model.create({
                "name":_("Accounting Systems"),
                "asset_type":"purchase",
                'prorata_computation_type': 'constant_periods',
                "state":"model",
                "method":"linear",
                 "method_number":24,
                 "method_period":"1",
                "journal_id":fa_journal.id,
                "account_asset_id":acc_sys_acc.id,
                "account_depreciation_id":acc_sys_dep_acc.id,
                "account_depreciation_expense_id":acc_sys_exp_acc.id,
                 "company_id":company.id
                })
            acc_sys._update_field_translations('name', {'ar_001': 'نظام المحاسبة'})
            
            acc_sys_acc.create_asset = "draft"
            acc_sys_acc.multiple_assets_per_line = False
            acc_sys_acc.asset_model = acc_sys.id  
            acc_sys_acc.allowed_journal_ids = [(6,0,[sale_journal.id,purchase_journal.id])]
            acc_sys_dep_acc.allowed_journal_ids = [(6,0,[fa_journal.id])]
            acc_sys_exp_acc.allowed_journal_ids = [(6,0,[fa_journal.id])]
            
        if fa_journal:
            taq_acc =self.env.ref("l10n_me.%s_account_account_template_26"%(company.id), False)
            if taq_acc:
                taq_acc.allowed_journal_ids = [(6, 0, [fa_journal.id])]
            eda_acc =self.env.ref("l10n_me.%s_account_account_template_97"%(company.id), False)
            if eda_acc:
                eda_acc.allowed_journal_ids = [(6, 0, [fa_journal.id])]
            fad_acc =self.env.ref("l10n_me.%s_account_account_template_16"%(company.id), False)
            if fad_acc:
                fad_acc.allowed_journal_ids = [(6, 0, [fa_journal.id])]    
            dad_acc =self.env.ref("l10n_me.%s_account_account_template_22"%(company.id), False)
            if dad_acc:
                dad_acc.allowed_journal_ids = [(6, 0, [fa_journal.id])]
            cad_acc =self.env.ref("l10n_me.%s_account_account_template_18"%(company.id), False)
            if cad_acc:
                cad_acc.allowed_journal_ids = [(6, 0, [fa_journal.id])]
            csad_acc =self.env.ref("l10n_me.%s_account_account_template_24"%(company.id), False)
            if csad_acc:
                csad_acc.allowed_journal_ids = [(6, 0, [fa_journal.id])]
            acad_acc =self.env.ref("l10n_me.%s_account_account_template_20"%(company.id), False)
            if acad_acc:
                acad_acc.allowed_journal_ids = [(6, 0, [fa_journal.id])]
            # furniture_acc =self.env.ref("l10n_me.%s_account_account_template_15"%(company.id), False)
            # if furniture_acc:
            #     print(furniture_acc.allowed_journal_ids.ids)
            #     jrnls = furniture_acc.allowed_journal_ids.ids + fa_journal.id
            #     furniture_acc.allowed_journal_ids = [(6, 0, jrnls)]
        
        prepaid_rent = env.ref("l10n_me.%s_account_account_template_12"%(company.id), False)
        if prepaid_rent:
            prepaid_rent.create_asset = "draft"
        
        prepaid_net = env.ref("l10n_me.%s_account_account_template_11"%(company.id), False)
        if prepaid_net:
            prepaid_net.create_asset = "draft"
        
        if prepaid_main:
            prepaid_main.create_asset = "draft"
        
        if prepaid_h_ins:
            prepaid_h_ins.create_asset = "draft"
    
    def _load(self, company):
        res = super(AccountChartTemplate, self)._load(company)
        if self.parent_id.id == self.env.ref("l10n_me.l10nme_chart_template").id or self.id == self.env.ref("l10n_me.l10nme_chart_template").id:
            self.load_account_assets(company)
        return res
        
        
        