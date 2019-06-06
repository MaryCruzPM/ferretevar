# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
from odoo import fields
from odoo import models
from odoo import api
# modelo de campos a editar desde factura borrados
class editable(models.Model):
	_inherit='res.partner'


	Banco_asociado = fields.Many2one('rest.partner.bank')		
	Metodo_pago = fields.Many2one('l10n_mx_edi.payment.method')
	Transferenciaelectronica_Uso = fields.Selection(selection=[('Adquisición de mercancías'),('Devoluciones, descuentos o bonificaciones'),
		('Gastos en general'),('Construcciones'),('Mobiliario y equipo de oficina por inversiones'),('Equipo de transporte'),('Equipo de cómputo y accesorios'),
		('Dados, troqueles, moldes, matrices y herramientas'),('Comunicaciones telefónicas'),('Comunicaciones satelitales'),('Otra maquinaria y equipo'),
		('Honorarios médicos,dentales y gastos hospitalarios'),('Gastos médicos por incapacidad o discapacidad'),('Gastos funerales'),('Donativos'),
		('Intereses reales efectivamente pagados '),('Aportaciones voluntarias al SAR.',('Primas por seguros de gastos médicos'),
			('Gastos de transportación escolar obligatoria'),('Depósitos en cuentas para el ahorro, primas que tengan como base de pensiones'),
			('pagos de servicios educativos (colegiaturas)'),('por definir'))],
		)
