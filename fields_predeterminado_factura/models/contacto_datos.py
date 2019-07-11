# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
from odoo import fields
from odoo import models
from odoo import api
# modelo de campos a editar desde factura borrados
class editable(models.Model):
	_inherit='res.partner'

	#asociado = fields.Many2one(related='id.bank_id')
	Banco_asociado = fields.Many2one('res.partner.bank')		
	Metodo_pago = fields.Many2one('l10n_mx_edi.payment.method')
	Transferenciaelectronica_Uso = fields.Selection(selection=[('G01','Adquisición de mercancías'),('G02','Devoluciones, descuentos o bonificaciones'),
		('G03','Gastos en general'),('l01','Construcciones'),('l02','Mobiliario y equipo de oficina por inversiones'),('l03','Equipo de transporte'),('l04','Equipo de cómputo y accesorios'),
		('l05','Dados, troqueles, moldes, matrices y herramientas'),('l06','Comunicaciones telefónicas'),('l07','Comunicaciones satelitales'),('l08','Otra maquinaria y equipo'),
		('D01','Honorarios médicos,dentales y gastos hospitalarios'),('D02','Gastos médicos por incapacidad o discapacidad'),('D03','Gastos funerales'),('D04','Donativos'),
		('D05','Intereses reales efectivamente pagados'),('D06','Aportaciones voluntarias al SAR.'),('D07','Primas por seguros de gastos médicos'),
		('D08','Gastos de transportación escolar obligatoria'),('D09','Depósitos en cuentas para el ahorro, primas que tengan como base de pensiones'),
		('D10','pagos de servicios educativos (colegiaturas)'),('P01','por definir')],
		)

	#Transferenciaelectronica_Uso_2= fields.Selection(related='invoice_ids.l10n_mx_edi_usage') #primer campo relacionado de este modelo respartner con  el otro modelo account de donde pertence el campo a donde queremos relacionarlo
