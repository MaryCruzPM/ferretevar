# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
from odoo import fields
from odoo import models
from odoo import api
# modelo de campos a editar desde factura borrados
class editable_campos_invoice(models.Model):
	_inherit='account.invoice'


	@api.depends('partner_id')
	def _ca(self):
		id_x= self.env['product.template'].search([('partner_id', '=', self.partner_id.id)])
		self.l10n_mx_edi_partner_bank_id=id_x.Banco_asociado	
		self.l10n_mx_edi_payment_method_id=id_x.Método_pago
		self.l10n_mx_edi_usage=id_x.Transferenciaelectrónica_Uso 




	# 	print(id_x.x_metros2)
	# 	self.110n_mx_edi_partner_bank_id=id_x.x_metros2
	# 	self.large=id_x.x_largo
	# 	self.wigth=id_x.x_ancho


	# @api.model
	# def create(self, values):
	# 	record = super(account.invoice, self).create(values)
	# 	idx=self.env['res.partner'].search(['partner_id','=',self.partner_id.id])
	# 	record.l10n_mx_edi_partner_bank_id=idx.Banco_asociado
	# 	record.l10n_mx_edi_payment_method_id=id_x.Método_pago
	#  	record.l10n_mx_edi_usage=id_x.Transferenciaelectrónica_Uso 

		# Override the original create function for the res.partner model
		


	  # @api.model
   #  def create(self, vals):

   #      rec=super(QuantityBudget, self).create(vals)
   #      total=self.search_count([('name', '=', rec.name.id), ('project_id', '=', rec.project_id.id)])
   #      if total>1:
   #          raise ValidationError(_('Product Category should not be repeat!'))
   #      return rec
		
		
		

	# @api.multi
 #    def _create_invoice(self, order, so_line, amount):
 #        inv_obj = self.env['account.invoice']
 #        ir_property_obj = self.env['ir.property']

 #        account_id = False
 #        if self.product_id.id:
 #            account_id = self.product_id.property_account_income_id.id or self.product_id.categ_id.property_account_income_categ_id.id
 #        if not account_id:
 #            inc_acc = ir_property_obj.get('property_account_income_categ_id', 'product.category')
 #            account_id = order.fiscal_position_id.map_account(inc_acc).id if inc_acc else False
 #        if not account_id:
 #            raise UserError(
 #                _('There is no income account defined for this product: "%s". You may have to install a chart of account from Accounting app,$
 #                (self.product_id.name,))

 #        if self.amount <= 0.00:
 #            raise UserError(_('The value of the down payment amount must be positive.'))
 #        context = {'lang': order.partner_id.lang}
 #        if self.advance_payment_method == 'percentage':
 #            amount = order.amount_untaxed * self.amount / 100
 #            name = _("Down payment of %s%%") % (self.amount,)
 #        else:
 #            amount = self.amount

 #        if not account_id:
 #            inc_acc = ir_property_obj.get('property_account_income_categ_id', 'product.category')
 #            account_id = order.fiscal_position_id.map_account(inc_acc).id if inc_acc else False
 #        if not account_id:
 #            raise UserError(
 #                _('There is no income account defined for this product: "%s". You may have to install a chart of account from Accounting app,$
 #                (self.product_id.name,))

 #        if self.amount <= 0.00:
 #            raise UserError(_('The value of the down payment amount must be positive.'))
 #        context = {'lang': order.partner_id.lang}
 #        if self.advance_payment_method == 'percentage':
 #            amount = order.amount_untaxed * self.amount / 100
 #            name = _("Down payment of %s%%") % (self.amount,)
 #        else:
 #            amount = self.amount
 #            name = _('Down Payment')
 #        del context
 #        taxes = self.product_id.taxes_id.filtered(lambda r: not order.company_id or r.company_id == order.company_id)
 #        if order.fiscal_position_id and taxes:
 #            tax_ids = order.fiscal_position_id.map_tax(taxes).ids
 #        else:
 #            tax_ids = taxes.ids

 #        invoice = inv_obj.create({
 #            'name': order.client_order_ref or order.name,
 #            'origin': order.name,
 #            'type': 'out_invoice',
 #            'reference': False,
 #            'account_id': order.partner_id.property_account_receivable_id.id,
 #            'partner_id': order.partner_invoice_id.id,
 #            'partner_shipping_id': order.partner_shipping_id.id,
 #            'invoice_line_ids': [(0, 0, {
 #                'name': name,
 #                'origin': order.name,
 #                'account_id': account_id,
 #                'price_unit': amount,
 #                'quantity': 1.0,
 #                'discount': 0.0,
 #                'uom_id': self.product_id.uom_id.id,
 #                'product_id': self.product_id.id,
 #                'sale_line_ids': [(6, 0, [so_line.id])],
 #                'invoice_line_tax_ids': [(6, 0, tax_ids)],
 #                'account_analytic_id': order.analytic_account_id.id or False,
 #            })],
 #            'currency_id': order.pricelist_id.currency_id.id,
 #            'payment_term_id': order.payment_term_id.id,
 #            'fiscal_position_id': order.fiscal_position_id.id or order.partner_id.property_account_position_id.id,
 #            'team_id': order.team_id.id,
 #            'user_id': order.user_id.id,
 #            'comment': order.note,
 #        })
 #        invoice.compute_taxes()
 #        invoice.message_post_with_view('mail.message_origin_link',
 #                    values={'self': invoice, 'origin': order},
 #                    subtype_id=self.env.ref('mail.mt_note').id)
 #        return invoice
