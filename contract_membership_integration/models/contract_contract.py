from odoo import fields
from odoo import models


class Contract(models.Model):
    _inherit = "contract.contract"

    membership_line_ids = fields.One2many(
        comodel_name="membership.membership_line",
        inverse_name="contract_line_id",
        string="Membership lines",
        compute="_compute_membership_line_ids",
        domain=[("state", "in", ["invoiced", "paid", "free"])],
    )

    def _compute_membership_line_ids(self):
        for record in self:
            membership_line_ids = record.contract_line_ids.mapped("membership_line_ids")
            record.membership_line_ids = membership_line_ids
