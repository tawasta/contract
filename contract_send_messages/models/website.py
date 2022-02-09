from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    contract_email_ids = fields.Many2many(
        comodel_name="res.partner",
        string="Contract email",
        help="when the contract is created, these people are added as successors",
    )
