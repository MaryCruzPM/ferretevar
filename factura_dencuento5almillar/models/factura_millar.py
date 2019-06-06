# -*- coding: utf-8 -*-

import json
import re
import uuid
from functools import partial

from lxml import etree
from dateutil.relativedelta import relativedelta
from werkzeug.urls import url_encode

from odoo import api, exceptions, fields, models, _
from odoo.tools import float_is_zero, float_compare, pycompat
from odoo.tools.misc import formatLang

from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning

from odoo.addons import decimal_precision as dp
import logging

_logger = logging.getLogger(__name__)

# mapping invoice type to journal type
TYPE2JOURNAL = {
    'out_invoice': 'sale',
    'in_invoice': 'purchase',
    'out_refund': 'sale',
    'in_refund': 'purchase',
}

# mapping invoice type to refund type
TYPE2REFUND = {
    'out_invoice': 'out_refund',        # Customer Invoice
    'in_invoice': 'in_refund',          # Vendor Bill
    'out_refund': 'out_invoice',        # Customer Credit Note
    'in_refund': 'in_invoice',          # Vendor Credit Note
}

MAGIC_COLUMNS = ('id', 'create_uid', 'create_date', 'write_uid', 'write_date')


class add_factura_millar(models.Model):
	_inherit = 'account.invoice'

	@api.one
	@api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'tax_line_ids.amount_rounding',
                   'currency_id', 'company_id', 'date_invoice', 'type','seleccionDescuento')


	def _compute_amount(self):
	        round_curr = self.currency_id.round
	        self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line_ids)      	
	        self.amount_tax = sum(round_curr(line.amount_total) for line in self.tax_line_ids)
	        activo=self.seleccionDescuento
	        print(activo)	        
	        if activo == True:
	        	print("hola")
	        	valormillar= 0.005 
	        	self.cantmillar = self.amount_untaxed * valormillar
	        	print("hola")
	        	self.amount_total = ((self.amount_untaxed + self.amount_tax) - self.cantmillar)
	        else:
	        	self.cantmillar=0.00
	        	print("hola")
	        	self.amount_total = self.amount_untaxed + self.amount_tax
	        amount_total_company_signed = self.amount_total
	        amount_untaxed_signed = self.amount_untaxed
	        if self.currency_id and self.company_id and self.currency_id != self.company_id.currency_id:
	            currency_id = self.currency_id.with_context(date=self.date_invoice)
	            amount_total_company_signed = currency_id.compute(self.amount_total, self.company_id.currency_id)
	            amount_untaxed_signed = currency_id.compute(self.amount_untaxed, self.company_id.currency_id)
	        sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
	        self.amount_total_company_signed = amount_total_company_signed * sign
	        self.amount_total_signed = self.amount_total * sign
	        self.amount_untaxed_signed = amount_untaxed_signed * sign

	# @api.one
 #    @api.depends(
 #        'state', 'currency_id', 'invoice_line_ids.price_subtotal',
 #        'move_id.line_ids.amount_residual',
 #        'move_id.line_ids.currency_id')

	# def _compute_residual(self):

	# 	residual = 0.0
	# 	residual_company_signed = 0.0
	# 	sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
	# 	for line in self.sudo().move_id.line_ids:
	# 		if line.account_id == self.account_id:
 #                residual_company_signed += line.amount_residual
 #                print(residual_company_signed)
 #                if line.currency_id == self.currency_id:

 #                	print("si la condicion es ==")
                	
 #                    residual += line.amount_residual_currency if line.currency_id else line.amount_residual
 #                    print(residual)
 #                else:
 #                	print("sino entonces")
 #                	print("imprime esto")

 #                    from_currency = (line.currency_id and line.currency_id.with_context(date=line.date)) or line.company_id.currency_id.with_$
 #                    residual += from_currency.compute(line.amount_residual, self.currency_id)
 #                    print(from_currency)
 #                    print(residual)
 #        self.residual_company_signed = abs(residual_company_signed) * sign
 #        self.residual_signed = abs(residual) * sign
 #        self.residual = abs(residual)
 #        digits_rounding_precision = self.currency_id.rounding
 #        if float_is_zero(self.residual, precision_rounding=digits_rounding_precision):
 #            self.reconciled = True
 #        else:
 #            self.reconciled = False







	seleccionDescuento = fields.Boolean()# campo para seleccionar si se requiere el descuento
	cantmillar = fields.Float() #cantidad calculada  0.0055

	amount_total = fields.Monetary(string='Total',
        store=True, readonly=True, compute='_compute_amount')

#
 	# residual = fields.Monetary(string='Amount Due',
  #       compute='_compute_residual', store=True, help="Remaining amount due.")


	


   # @api.multi
   #  def action_invoice_open(self):
   #      # lots of duplicate calls to action_invoice_open, so we remove those already open
   #      Print("ejecuatando codigo de boton")
   #      to_open_invoices = self.filtered(lambda inv: inv.state != 'open')
   #      if to_open_invoices.filtered(lambda inv: inv.state != 'draft'):
   #          raise UserError(_("Invoice must be in draft state in order to validate it."))
   #      if to_open_invoices.filtered(lambda inv: float_compare(inv.amount_total, 0.0, precision_rounding=inv.currency_id.rounding) == -1):
   #          raise UserError(_("You cannot validate an invoice with a negative total amount. You should create a credit note instead."))
   #      to_open_invoices.action_date_assign()
   #      to_open_invoices.action_move_create()
   #      return to_open_invoices.invoice_validate()
