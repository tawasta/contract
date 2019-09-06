
from odoo import models, fields


import logging
logger = logging.getLogger(__name__)


class AccountAnalyticContract(models.Model):
    _inherit = 'account.analytic.contract'

    partner_shipping_id = fields.Many2one(
        comodel_name="res.partner",
        string="Delivery Address",
    )
