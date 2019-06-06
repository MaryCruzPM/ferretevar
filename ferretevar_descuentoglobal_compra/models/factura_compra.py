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



class add_descuento_global(models.Model):
	"""docstring for ClassName"""
	_inherit='account.invoice'


	# @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'tax_line_ids.amount_rounding',
 #                 'currency_id', 'company_id', 'date_invoice', 'type')
 #    def _compute_amount(self):
 #        round_curr = self.currency_id.round
 #        self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line_ids)
 #        self.amount_tax = sum(round_curr(line.amount_total) for line in self.tax_line_ids)
 #        self.amount_total = self.amount_untaxed + self.amount_tax
 #        amount_total_company_signed = self.amount_total
 #        amount_untaxed_signed = self.amount_untaxed
 #        if self.currency_id and self.company_id and self.currency_id != self.company_id.currency_id:
 #            currency_id = self.currency_id.with_context(date=self.date_invoice)
 #            amount_total_company_signed = currency_id.compute(self.amount_total, self.company_id.currency_id)
 #            amount_untaxed_signed = currency_id.compute(self.amount_untaxed, self.company_id.currency_id)
 #        sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
 #        self.amount_total_company_signed = amount_total_company_signed * sign
 #        self.amount_total_signed = self.amount_total * sign
 #        self.amount_untaxed_signed = amount_untaxed_signed * sign

 	def _compute_amount(self):
 		print("holaaaaaaaa wowwww")

 	amount_untaxed = fields.Monetary(string='Untaxed Amount', 
 		store=True, readonly=True, compute='_compute_amount', track_visibility='always')
   # amount_untaxed = fields.Monetary(string='Untaxed Amount',
    #    store=True, readonly=True, compute='_compute_amount', track_visibility='always')
    
    amount_tax = fields.Monetary(string='Tax',
        store=True, readonly=True, compute='_compute_amount')
    amount_total = fields.Monetary(string='Total',
        store=True, readonly=True, compute='_compute_amount')
  
# @api.model
#     def create(self, vals):
#         onchanges = {
#             '_onchange_partner_id': ['account_id', 'payment_term_id', 'fiscal_position_id', 'partner_bank_id'],
#             '_onchange_journal_id': ['currency_id'],
#         }
#         for onchange_method, changed_fields in onchanges.items():
#             if any(f not in vals for f in changed_fields):
#                 invoice = self.new(vals)
#                 getattr(invoice, onchange_method)()
#                 for field in changed_fields:
#                     if field not in vals and invoice[field]:
#                         vals[field] = invoice._fields[field].convert_to_write(invoice[field], invoice)
#         if not vals.get('account_id',False):
#             raise UserError(_('Configuration error!\nCould not find any account to create the invoice, are you sure you have a chart of accou$

#         invoice = super(AccountInvoice, self.with_context(mail_create_nolog=True)).create(vals)

#         if any(line.invoice_line_tax_ids for line in invoice.invoice_line_ids) and not invoice.tax_line_ids:
#             invoice.compute_taxes()

#         return invoice

    # @api.multi
    # def action_invoice_open(self):
    #     # lots of duplicate calls to action_invoice_open, so we remove those already open
    #     to_open_invoices = self.filtered(lambda inv: inv.state != 'open')
    #     if to_open_invoices.filtered(lambda inv: inv.state != 'draft'):
    #         raise UserError(_("Invoice must be in draft state in order to validate it."))
    #     if to_open_invoices.filtered(lambda inv: float_compare(inv.amount_total, 0.0, precision_rounding=inv.currency_id.rounding) == -1):
    #         raise UserError(_("You cannot validate an invoice with a negative total amount. You should create a credit note instead."))
    #     to_open_invoices.action_date_assign()
    #     to_open_invoices.action_move_create()
    #     return to_open_invoices.invoice_validate()


# @api.multi
#     def action_invoice_draft(self):
#         if self.filtered(lambda inv: inv.state != 'cancel'):
#             raise UserError(_("Invoice must be cancelled in order to reset it to draft."))
#         # go from canceled state to draft state
#         self.write({'state': 'draft', 'date': False})
#         # Delete former printed invoice
#         try:
#             report_invoice = self.env['ir.actions.report']._get_report_from_name('account.report_invoice')
#         except IndexError:
#             report_invoice = False
#         if report_invoice and report_invoice.attachment:
#             for invoice in self:
#                 with invoice.env.do_in_draft():
#                     invoice.number, invoice.state = invoice.move_name, 'open'
#                     attachment = self.env.ref('account.account_invoices').retrieve_attachment(invoice)
#                 if attachment:
#                     attachment.unlink()
#         return True


#   @api.one
# 	def generate_descuento(self):
# 	    #Generates a random name between 9 and 15 characters long and writes it to the record.
# 	    #self.write({'name': ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(randint(9,15)))})
# 	#	print("perfectooooooooooooooo")
# 		porcentajeT = 100 # porcentaje total 
# 		iva = 16 # 16 % de iva

# 		for order in self:
# 			amount_untaxed = amount_tax = 0.0
# 			for line in order.order_line:
# 				amount_untaxed += line.price_subtotal #recorremos las orden de lineas y se va sumando 
# 				amount_tax += line.price_tax # recorremos las orden de lineas y se va sumando 
# 				print("subtotal0")
# #				print(self.x_subtotal)
# 				print(self.amount_untaxed)
# 				self.x_subtotal=amount_untaxed # insertamos el subotal de variable original  a la variable nueva para el dubtotal sin descuento
# 				if(self.x_seleccion == "porcentaje"): #se pregunta el campo si es porcentaje para hacer le decuento por porcentaje
# 					print("hola")

# #					self.x_subtotal=self.amount_untaxed #suma de la ordeline sin iva y sin descuento
# 					self.x_cantDescuento=(self.x_subtotal * self.x_cantidadPorcentaje) / porcentajeT
# 					self.amount_untaxed=self.x_subtotal - self.x_cantDescuento
# 					self.amount_tax=(self.amount_untaxed*iva)/porcentajeT
# 					self.amount_total=self.amount_untaxed+self.amount_tax

							
# 				if (self.x_seleccion == "importe"):
# 					print(self.amount_untaxed)
# #					self.x_subtotal=self.amount_untaxed
# 					print(self.x_seleccion)
# 					self.x_cantDescuento=self.x_cantidadPorcentaje
# 					self.amount_untaxed=self.x_subtotal - self.x_cantDescuento
# 					self.amount_tax=(self.amount_untaxed*iva)/porcentajeT
# 					self.amount_total=self.amount_untaxed+self.amount_tax

							
# 				if(self.x_seleccion != "importe" and self.x_seleccion != "porcentaje"): 
# 					self.x_subtotal = 0.0
# 					self.x_cantDescuento = 0.0
# #					self.x_cantidadPorcentaje=0.0
# 					order.update({
# 	                'amount_untaxed': order.currency_id.round(amount_untaxed),
#                     'amount_tax': order.currency_id.round(amount_tax),
# 	                'amount_total': amount_untaxed + amount_tax,
#  		            })



# nano /odoo/odoo-server/addons/account/models/account_invoice.py
