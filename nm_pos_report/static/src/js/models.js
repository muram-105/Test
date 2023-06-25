/* global Sha1 */
odoo.define('nm_pos_report.models', function (require) {
	
	var { Orderline ,Payment, Order} = require('point_of_sale.models');
	const Registries = require('point_of_sale.Registries');


	const ProductArabic = (Orderline) => class ProductArabic extends Orderline {
	    export_for_printing() {
	        var line = super.export_for_printing(...arguments);
	        line.product_name_ar = this.get_product().name_ar;
			line.reference = this.get_product().default_code;
	        return line;
	    }
	}
	
	const PaymentExt = (Payment) => class PaymentExt extends Payment {
	    export_for_printing() {
	        var pay = super.export_for_printing(...arguments);
	        pay.name_ar = this.payment_method.name_ar;
	        return pay;
	    }
	}
	
	const OrderEXT = (Order) => class OrderEXT extends Order {
	    export_for_printing() {
	        var order = super.export_for_printing(...arguments);
	        var tot_qty = 0;
	        for (var i = 0; i < order.orderlines.length; i++) {
	        	tot_qty += order.orderlines[i].quantity;
	        }
	        order.tot_qty = tot_qty;
	        return order;
	    }
	}
	
	Registries.Model.extend(Orderline, ProductArabic);
	Registries.Model.extend(Order, OrderEXT);
	Registries.Model.extend(Payment, PaymentExt);
    
});
