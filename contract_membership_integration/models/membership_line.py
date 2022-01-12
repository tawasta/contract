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

    @api.model
    def create(self, vals):
        # Override the partner: use contract partner if membership is created from a contract
        if "account_invoice_line" in vals:
            ail = (
                self.env["account.move.line"]
                .sudo()
                .browse([vals["account_invoice_line"]])
            )
            if ail.contract_line_id:
                vals["partner"] = ail.contract_line_id.contract_id.partner_id.id
        res = super().create(vals)

        return res

    def write(self, vals):
        if vals.get("partner") and len(self) > 1:
            for record in self:
                if record.contract_line_id:
                    record.partner = record.contract_line_id.contract_id.partner_id
                else:
                    record.partner = vals["partner"]

            vals.pop("partner")

        return super().write(vals)
