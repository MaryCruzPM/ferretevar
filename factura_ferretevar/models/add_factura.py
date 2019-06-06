# -*- coding: utf-8 -*-

from odoo import fields, models, api

class add_field_factura(models.Model):
	_inherit = 'account.invoice'

	x_nota = fields.Text(string='Observaciones')
	