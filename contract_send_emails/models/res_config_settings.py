from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    contract_email = fields.Char(related='website_id.contract_email', readonly=False, help="When the contract line is terminated or updated, a message will be sent to this email")
