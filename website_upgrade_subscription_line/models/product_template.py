from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    change_allowed = fields.Boolean(string="Change allowed", default=False)
