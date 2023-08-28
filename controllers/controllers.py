# -*- coding: utf-8 -*-
# from odoo import http


# class Riders(http.Controller):
#     @http.route('/riders/riders', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/riders/riders/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('riders.listing', {
#             'root': '/riders/riders',
#             'objects': http.request.env['riders.riders'].search([]),
#         })

#     @http.route('/riders/riders/objects/<model("riders.riders"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('riders.object', {
#             'object': obj
#         })
