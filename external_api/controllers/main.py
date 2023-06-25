# -*- coding: utf-8 -*-
import logging

from odoo import http, fields
from odoo.http import request
from odoo.tools import DEFAULT_SERVER_TIME_FORMAT as TIME_FORMAT

_logger = logging.getLogger(__name__)


class ExternalApi(http.Controller):

    @http.route('/get_stock_data', type='json', auth='none', methods=['GET', 'POST'])
    def get_stock_data(self, **kwargs):
        context_today = fields.Date.context_today
        to_string = fields.Date.to_string
        sm_obj = request.env['stock.move'].with_context(tz='Asia/Doha')
        move_ids = sm_obj.sudo().search(
            [('state', '=', 'done'),
             '|',
             ('location_id.sync', '=', True),
             ('location_dest_id.sync', '=', True),
             '|',
             '&',
             ('location_id.usage', '=', 'internal'),
             ('location_dest_id.usage', '!=', 'internal'),
             '&',
             ('location_id.usage', '!=', 'internal'),
             ('location_dest_id.usage', '=', 'internal')
             ])
        stock_list = []
        for move_id in move_ids:
            is_in = move_id.location_dest_id.usage == 'internal'
            sign = is_in and 1 or -1
            stock_list.append({"transfer_date": to_string(context_today(move_id, move_id.date)),
                               'production_place': (is_in and move_id.location_dest_id or move_id.location_id).barcode,
                               'article_number': move_id.product_id.default_code,
                               'unit': move_id.product_uom.name,
                               'quantity': move_id.product_qty * sign,
                               'cost': sum(move_id.stock_valuation_layer_ids.mapped('value')),
                               'currency': move_id.company_id.currency_id.name
                               })
        return stock_list

    @http.route('/get_sales_data', type='json', auth='none', methods=['GET', 'POST'])
    def get_sales_data(self, **kwargs):
        pos_line_ids = request.env['pos.order.line'].with_context(tz='Asia/Doha').sudo().search(
            [('order_id.state', 'in', ('paid', 'done', 'invoiced')),
             ('order_id.config_id.picking_type_id.default_location_src_id.sync', '=', True)], order="id asc")
        sale_list = []
        context_today = fields.Date.context_today
        to_string = fields.Date.to_string
        for line in pos_line_ids:
            date_done = line.order_id.picking_ids and line.order_id.picking_ids[0].date_done or False
            if date_done:
                date_done = to_string(context_today(line, date_done))
            sale_hour = sale_date = date_order = line.order_id.date_order or False
            if date_order:
                sale_date = to_string(context_today(line, date_order))
                sale_hour = date_order.strftime(TIME_FORMAT)
            sale_list.append({
                'transfer_date': date_done,
                'sale_date': sale_date,
                'sale_hour': sale_hour,
                'production_place': line.order_id.config_id.picking_type_id.default_location_src_id.barcode or '',
                'article_number': line.product_id.default_code,
                'quantity': line.qty,
                'unit': line.product_uom_id.name,
                'cost_of_sale': line.total_cost,
                'sale_price': line.price_subtotal_incl,
                'currency': line.currency_id.name

            })
        return sale_list
