from odoo import api
from odoo import fields
from odoo import models


class MembershipLine(models.Model):

    _inherit = "membership.membership_line"

    contract_line_id = fields.Many2one(
        comodel_name="contract.line",
        string="Contract line",
        compute="_compute_contract_line_id",
        store=True,
    )

    @api.depends("account_invoice_line")
    def _compute_contract_line_id(self):
        for rec in self:
            if rec.account_invoice_line:
                rec.contract_line_id = rec.account_invoice_line.contract_line_id
            else:
                rec.contract_line_id = False
