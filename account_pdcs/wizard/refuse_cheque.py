# -*- coding: utf-8 -*-
from odoo import models, fields, _
from itertools import groupby


class RefuseChequesAction(models.TransientModel):
    _name = 'refuse.cheque.action'
    _description = "Refuse Cheques Action"

    unreconcile = fields.Boolean('Show in Bank Statement?',
                                 help="If checked, outstanding entries will not be reconciled and will appear in your bank statement reconciliation")
    date = fields.Date("Date",required=True, defaulte=fields.Date.context_today)

    def refuse_cheque(self):
        account_payment = self.env['account.payment']
        paymrnt_ids = account_payment.browse(self._context.get('active_ids', []))
        self = self.with_context(skip_check_payment_moves=True)
        rv_obj = self.env['account.move.reversal']
        for payment in paymrnt_ids.filtered(lambda x: x.state == 'posted' and x.cheque_state != 'refused'
                                            and not x.inverse_move_id):
            res = {}

            if payment.payment_type == 'outbound':
                rv_id = rv_obj.with_context({'default_date': self.date,
                                             'active_model': 'account.move',
                                             'default_journal_id': payment.journal_id.id,
                                             'active_ids': payment.move_id.ids}).create({})
                rv_id.reverse_moves()
                inverse_move_id = rv_id.new_move_ids
                if payment.move_id.ref:
                    inverse_move_id.ref = inverse_move_id.ref + ' ' + payment.move_id.ref
                if inverse_move_id.auto_post:
                    inverse_move_id.auto_post = False
                    inverse_move_id.action_post()
                if self.unreconcile:
                    inverse_move_id.line_ids.filtered(lambda x:x.account_id != payment.destination_account_id).remove_move_reconcile()
            else:
                def dest_acc_key(x): return x.account_id == payment.destination_account_id
                dest_line_id = payment.move_id.line_ids.filtered(dest_acc_key)
                dest_line_id.remove_move_reconcile()
                vals = {
                    'name': False,
                    'partner_id': payment.partner_id.id,
                    'journal_id': payment.journal_bank_id.id,
                    'date': self.date,
                    'ref': 'Refusal of %s' % (payment.ref or payment.name),
                }
                dr, cr = payment.get_move_lines_dr_cr()
                dr['account_id'] = payment.destination_account_id.id
                cr['account_id'] = (payment.last_payment_method_line_id.payment_account_id or
                                    payment.company_id.account_journal_payment_debit_account_id
                                    if payment.last_payment_method_line_id
                                    else payment.outstanding_account_id).id
                vals['line_ids'] = [(0, 0, dr), (0, 0, cr)]
                inverse_move_id = self.env['account.move'].create(vals)
                inverse_move_id.action_post()
                i_dest_line_id = inverse_move_id.line_ids.filtered(dest_acc_key)
                (dest_line_id|i_dest_line_id).reconcile()
                if not self.unreconcile:
                    journal_line_id = inverse_move_id.line_ids - i_dest_line_id
                    (journal_line_id | payment.route_move_id.line_ids.filtered(
                        lambda x:x.account_id == journal_line_id.account_id)).reconcile()


            res['inverse_move_id'] = inverse_move_id.id


            res and payment.write(res)

        return {'type': 'ir.actions.act_window_close'}
