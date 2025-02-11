# models/alquiler_producto.py
from odoo import models, fields, api
from datetime import timedelta

class AlquilerProducto(models.Model):
    _name = 'alquiler.producto'
    _description = 'Alquiler de Productos'

    cliente_id = fields.Many2one('res.partner', string='Cliente', required=True)
    producto_id = fields.Many2one('product.product', string='Producto', required=True)
    fecha_inicio = fields.Date(string='Fecha de Inicio', required=True, 
                             default=fields.Date.context_today)
    fecha_fin = fields.Date(string='Fecha de Fin', compute='_compute_fecha_fin', 
                          store=True)
    estado = fields.Selection([
        ('alquiler', 'En Alquiler'),
        ('entregado', 'Entregado'),
        ('no_entregado', 'No Entregado')
    ], string='Estado', default='alquiler', required=True)
    observaciones = fields.Text(string='Observaciones')
    
    @api.depends('fecha_inicio')
    def _compute_fecha_fin(self):
        for record in self:
            if record.fecha_inicio:
                record.fecha_fin = record.fecha_inicio + timedelta(days=30)

    @api.onchange('producto_id')
    def _onchange_producto(self):
        if self.producto_id:
            alquileres_activos = self.env['alquiler.producto'].search_count([
                ('producto_id', '=', self.producto_id.id),
                ('estado', '=', 'alquiler')
            ])
            if alquileres_activos > 0:
                return {'warning': {
                    'title': 'Advertencia',
                    'message': 'Este producto ya está en alquiler'
                }}
            
    def _check_alquileres_vencidos(self):
        alquileres = self.search([
            ('estado', '=', 'alquiler'),
            ('fecha_fin', '<', fields.Date.today())
        ])
        alquileres.write({'estado': 'no_entregado'})