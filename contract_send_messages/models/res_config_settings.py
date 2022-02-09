from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    contract_email_ids = fields.Many2many(
        related="website_id.contract_email_ids",
        comodel_name="res.partner",
        readonly=False,
        help="when the contract is created, these people are added as successors",
    )
