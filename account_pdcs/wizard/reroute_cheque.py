# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


class RerouteChequesAction(models.TransientModel):
    _name = 'reroute.cheque.action'
    _description = "Reroute Cheques Action"

    date = fields.Date('Date', required=True, default=fields.Date.context_today)
    journal_id = fields.Many2one('account.journal', 'Route',
                                 domain="[('id', 'in', available_journal_ids)]", required=True)
    payment_method_line_id = fields.Many2one('account.payment.method.line', 'Payment Method',
                                             required=True, domain="[('journal_id', '=', journal_id),"
                                                                   "('payment_type', '=', 'inbound')]")
    available_journal_ids = fields.Many2many('account.journal', compute="_compute_available_journal_ids")

    def get_payments(self):
        payment_ids = self.env['account.payment'].browse(self._context.get('active_ids', []))
        domain = ['|', '|', ('cheque_state', 'not in', ['in_cheque_box', 'under_collection']),
                  ('state', '!=', 'posted'), ('payment_type', '!=', 'inbound')]
        if payment_ids.filtered_domain(domain):
            raise UserError(
                "All payments should be Posted & Cheque Status is 'In Cheques Box' or 'Under Collection' & Payment Type is 'Receive Money'")
        journal_ids = self.env['account.journal']
        for pay in payment_ids:
            journal_ids |= pay.journal_bank_id or pay.journal_id
        if len(journal_ids) > 1:
            raise UserError("Please make sure all selected payments have the same Cheque Route.")
        return payment_ids

    @api.depends_context('active_id')
    @api.depends('date')
    def _compute_available_journal_ids(self):
        self.ensure_one()
        journal_ids = [p.journal_bank_id.id or p.journal_id.id for p in self.get_payments()]
        self.available_journal_ids = self.env['account.journal'].search([('type', '=', 'bank'),
                                                                         ('id', 'not in', journal_ids)])

    def reroute_cheque(self):
        for payment_id in self.get_payments():
            if payment_id.route_move_id and payment_id.route_move_id.date > self.date:
                raise UserError("The date mustn't be less than last route's date")
            vals = {
                'name': False,
                'partner_id': payment_id.partner_id.id,
                'journal_id': self.journal_id.id,
                'date': self.date,
                'ref': 'Reroute of %s' % (payment_id.ref or payment_id.name),
            }
            dr, cr = payment_id.get_move_lines_dr_cr()
            dr['account_id'] = (self.payment_method_line_id.payment_account_id or
                                payment_id.company_id.account_journal_payment_debit_account_id).id
            cr['account_id'] = (payment_id.last_payment_method_line_id.payment_account_id or
                                payment_id.company_id.account_journal_payment_debit_account_id
                                if payment_id.last_payment_method_line_id
                                else payment_id.outstanding_account_id).id

            def key(x):
                return x.account_id.id == cr['account_id']

            line_id = (payment_id.route_move_id or payment_id.move_id).line_ids.filtered(key)
            vals['line_ids'] = [(0, 0, dr), (0, 0, cr)]
            move_id = self.env['account.move'].create(vals)
            move_id.action_post()
            (move_id.line_ids.filtered(key) | line_id).reconcile()
            payment_id.write(
                {'route_move_ids': [(4, move_id.id)], 'last_payment_method_line_id': self.payment_method_line_id})
        return {'type': 'ir.actions.act_window_close'}
