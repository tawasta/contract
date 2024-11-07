from odoo import models
from odoo.exceptions import AccessError


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"
