# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class Orders(models.Model):
    _name = 'riders.orders'
    _description = 'Permite definir las órdenes que usan los riders'

    id = fields.Integer(string='ID', required=True, readonly=True, copy=False,
                        default=lambda self: self.env['ir.sequence'].next_by_code('riders.orders.sequence'))
    pickUp_point = fields.Char(string='Punto de recogida', required=True)
    delivery_point = fields.Char(string='Punto de entrega', required=True)
    hour = fields.Datetime(string='Hora', required=True)
    date = fields.Date(string='Fecha', required=True)
    state = fields.Selection([
        ('send', 'Enviado'),
        ('canceled', 'Cancelado'),
        ('process', 'Elaborando'),
        ('delivered', 'Entregado')
    ], string='Estado del pedido')

    payment = fields.Selection([
        ('tarjeta', 'Tarjeta'),
        ('cash', 'Efectivo'),
        ('subscripcion', 'Subscripción')
    ], string='Forma de pago')

    price = fields.Float('Precio', (5, 2), help='Valor del pedido')
    discount = fields.Boolean('Descuento', default=False, required=True)
    discount_percentage = fields.Float('Porcentaje de descuento', (5, 2))
    final_price = fields.Float('Precio final', (5, 2), compute='_compute_final_price')

    # Relación entre clases
    drivers_ids = fields.Many2one('riders.drivers', string='Conductor')
    routes_id = fields.Many2one('riders.routes', string='Ruta')

    # API DE DESCUENTO
    @api.depends('price', 'discount', 'discount_percentage')
    def _compute_final_price(self):
        for order in self:
            if order.discount:
                discount_amount = order.price * (order.discount_percentage / 100)
                order.final_price = order.price - discount_amount
            else:
                order.final_price = order.price

    # DEF NOMBRE CALENDARIO
    def name_get(self):
        resultados = []
        for orders in self:
            descripcion = f'{len(orders.drivers_ids)} drivers - {orders.pickUp_point}'
            resultados.append((orders.id, descripcion))
            return resultados


class Drivers(models.Model):
    _name = 'riders.drivers'
    _description = 'Permite definir a los Driver y sus datos'
    _order = 'state'

    photo = fields.Image(string='Foto')
    name = fields.Char(string='Nombre del conductor', required=True)
    last_name = fields.Char(string='Apellidos', required=True)
    birth_date = fields.Date(string='Fecha de nacimiento', required=True)
    age = fields.Integer(string='Edad', compute='_get_age', store=True)
    telephone = fields.Char(string='Telefono', required=True)
    id_doc = fields.Char(string='Numero documento', required=True, help='Número de documento de identidad')
    registration_date = fields.Date('Fecha de alta', required=True)
    discharge_date = fields.Date('Fecha de baja', required=False)
    address = fields.Char(string='Direccion', required=True)
    average_rate = fields.Float('Calificacion media', (3, 1), default=0.0)
    vehicle = fields.Selection([('bici', 'Bicicleta'),
                                ('moto', 'Motocicleta'),
                                ('coche', 'coche'),
                                ('otro', 'Otro tipo de vehiculo')],
                               string='Tipo de vehículo')
    state = fields.Selection([('busy', 'Ocupado'),
                              ('free', 'Libre'),
                              ('vacation', 'Vacaciones'),
                              ('baja', 'Baja')], default='free',
                             string='Estado del repartidor')
    description = fields.Text(string='Breve descripcion personal')
    code = fields.Char(string='Código', compute='_compute_code', store=True)
    # Relacion entre clases
    orders_id = fields.One2many('riders.orders', 'drivers_ids', string='Ordenes')

    # GENERACION DE CODIGO DRIVERS
    @api.depends('name', 'last_name')
    def _compute_code(self):
        for driver in self:
            if driver.name and driver.last_name:
                driver.code = 'D-' + driver.name[:3].upper() + driver.last_name[:3].upper()

    # GENERACION EDAD
    @api.depends('birth_date')
    def _get_age(self):
        for driver in self:
            if driver.birth_date:
                today = fields.Date.today()
                delta = relativedelta(today, driver.birth_date)
                driver.age = delta.years
            else:
                driver.age = 0

    # RESTRICCION DE EDAD
    _sql_constraints = [('check_age_constraint', 'CHECK (age >= 18)', 'El conductor debe ser mayor de edad.')]


class Routes(models.Model):
    _name = 'riders.routes'
    _description = 'Permite definir las rutas que recorrerán los drivers'
    _order = 'duration'

    name = fields.Char(string='Nombre de la ruta', required=True)
    duration = fields.Float('Duracion del recorrido de la ruta', (3, 1), default=0.0)
    length = fields.Float('Distancia del recorrido de la ruta', (3, 1), default=0.0)
    address = fields.Char(string='Punto de recogida', required=True)

    # Relacion entre clases
    drivers_ids = fields.Many2many('riders.drivers', 'routes_id', string='Drivers')
    orders_id = fields.One2many('riders.orders', 'routes_id', string='Ordenes')
