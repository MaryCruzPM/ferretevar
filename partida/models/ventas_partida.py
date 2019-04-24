# -*- coding:utf-8 -*-
from odoo import fields
from odoo import models
from odoo import api


class ventas_heredadop(models.Model):
	"""docstring for ClassName"""
	_inherit='sale.order'

	@api.model
	def create(self, vals):
		value=1
		print("value = 1")
		new_id = super(ventas_heredadop, self).create(vals)
		print("creando los valore del sale order y pasandolo a new_id")
		for line in new_id.order_line: #se itera con el campo que esta relacionado que es order line, en este caso es porque este campo esta relacionado sale.order con sale,order.line
			line.x_num_partida=value 			
			print("valor de value cambiante")
			print(+value)			
			value=value+1
		return new_id		#en el metodo create es forzozo que lleve el return porque sino marca error


	@api.multi
	def write(self, vals):
		value=1
		ac=super(ventas_heredadop,self).write(vals) #el metodo write regresa un boolean que indica un true o un false si fue cambiado el campo
		for record in self.order_line:
			record.x_num_partida = value
			value=value+1		
		return ac


#las variables globales se declaran fuera de la clase y donde se ocupa global value en inicio dentro de la clase y despues ya se utiliza normalmente
	
# 		return new_id		#en el metodo create es forzozo que lleve el return porque sino marca error

   	


