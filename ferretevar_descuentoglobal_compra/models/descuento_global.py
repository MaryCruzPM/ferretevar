# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.exceptions import UserError, AccessError
from odoo.tools.misc import formatLang
from odoo.addons.base.res.res_partner import WARNING_MESSAGE, WARNING_HELP
from odoo.addons import decimal_precision as dp


class add_descuento_global(models.Model):
	"""docstring for ClassName"""
	_inherit='purchase.order'



	x_subtotal=fields.Float(
						String="subtotal total es cantidad de todo aun sin el descuento",
						)
	x_cantDescuento=fields.Float(
						String="cantidad a descontar de x_subtotal",#compute='_compute_calcula_descuento'
						)

#	x_cantidadimporte=fields.Float(
#						String="x_cantidad es el  porcentaje a descontar al subtotal o el importe",
#						)
	x_cantidadPorcentaje=fields.Float(
						String="x_cantidad es el  porcentaje a descontar al subtotal o el importe",
						)
	
	x_seleccion=fields.Selection(selection=[('porcentaje','Porcentaje'),('importe','Importe')],
			
		)# campo para seleccionar el descuento por importe o por porcentaje
	
	x_aplica_descuento = fields.Boolean(default='click descuento') #bandera boton para aplicar descuento

	@api.one
	def generate_descuento(self):
	    #Generates a random name between 9 and 15 characters long and writes it to the record.
	    #self.write({'name': ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(randint(9,15)))})
	#	print("perfectooooooooooooooo")
		porcentajeT = 100 # porcentaje total 
		iva = 16 # 16 % de iva

		for order in self:
			amount_untaxed = amount_tax = 0.0
			for line in order.order_line:
				amount_untaxed += line.price_subtotal #recorremos las orden de lineas y se va sumando 
				amount_tax += line.price_tax # recorremos las orden de lineas y se va sumando 
				print("subtotal0")
#				print(self.x_subtotal)
				print(self.amount_untaxed)
				self.x_subtotal=amount_untaxed # insertamos el subotal de variable original  a la variable nueva para el dubtotal sin descuento
				if(self.x_seleccion == "porcentaje"): #se pregunta el campo si es porcentaje para hacer le decuento por porcentaje
					print("hola")

#					self.x_subtotal=self.amount_untaxed #suma de la ordeline sin iva y sin descuento
					self.x_cantDescuento=(self.x_subtotal * self.x_cantidadPorcentaje) / porcentajeT
					self.amount_untaxed=self.x_subtotal - self.x_cantDescuento
					self.amount_tax=(self.amount_untaxed*iva)/porcentajeT
					self.amount_total=self.amount_untaxed+self.amount_tax

							
				if (self.x_seleccion == "importe"):
					print(self.amount_untaxed)
#					self.x_subtotal=self.amount_untaxed
					print(self.x_seleccion)
					self.x_cantDescuento=self.x_cantidadPorcentaje
					self.amount_untaxed=self.x_subtotal - self.x_cantDescuento
					self.amount_tax=(self.amount_untaxed*iva)/porcentajeT
					self.amount_total=self.amount_untaxed+self.amount_tax

							
				if(self.x_seleccion != "importe" and self.x_seleccion != "porcentaje"): 
					self.x_subtotal = 0.0
					self.x_cantDescuento = 0.0
#					self.x_cantidadPorcentaje=0.0
					order.update({
	                'amount_untaxed': order.currency_id.round(amount_untaxed),
                    'amount_tax': order.currency_id.round(amount_tax),
	                'amount_total': amount_untaxed + amount_tax,
 		            })



