# -*- coding: utf-8 -*-

import json
import re
import uuid
from functools import partial

from lxml import etree
from dateutil.relativedelta import relativedelta
from werkzeug.urls import url_encode

from odoo import api, exceptions, fields, models
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


	amount_untaxed = fields.Monetary(string='Amount Untaxed',compute='_commpute_amount',
		store=True,readonly=True, track_visibility='always')

	amount_tax = fields.Monetary(string='Tax', store=True, readonly=True, compute='_commpute_amount')

#	amount_total = fields.Monetary(string='Tax', store=True,readonly=True, compute='_commpute_amount')

	amount_tx=fields.Monetary(related = 'purchase_id.amount_total')

	x_aplica_descuento = fields.Boolean(related ='purchase_id.amount_total') #bandera boton para aplicar descuento



	@api.depends('invoice_line_ids.price_subtotal','tax_line_ids.amount','tax_line_ids.amount_rounding',
 		'currency_id','company_id','date_invoice','type')
	def _compute_amount(self):
 		print("holaaa wooooooo")
 		print(self.amount_tx)
 		round_curr =self.currency_id.round
 		self.amount_untaxed = sum (line.price_subtotal for line in self.invoice_line_ids)
 		self.amount_tax = sum(round_curr(line.amount_total) for line in self.tax_line_ids)
 		self.amount_total = self.amount_untaxed + self.amount_tax
 		amount_total_company_signed = self.amount_total
 		print(self.amount_total)
 		amount_untaxed_signed = self.amount_untaxed
 		if self.currency_id and self.company_id and self.currency_id != self.company_id.currency_id:
 			currency_id = self.currency_id.with_context(date=self.date_invoice)
 			amount_total_company_signed = currency_id.compute(self.amount_total,self.company_id.currency_id)
 			amount_untaxed_signed = currency_id.compute(self.amount_untaxed,self.company_id.currency_id)
 		sign=self.type in ['in_refund','out_refund'] and -1 or 1
 		self.amount_total_company_signed = amount_total_company_signed * sign
 		self.amount_total_signed = self.amount_total * sign
 		self.amount_untaxed_signed = amount_untaxed_signed * sign

 		