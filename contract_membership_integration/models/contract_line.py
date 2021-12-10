from odoo import fields
from odoo import models


class ContractLine(models.Model):
    _inherit = "contract.line"

    membership_line_ids = fields.One2many(
        comodel_name="membership.membership_line",
        inverse_name="contract_line_id",
        string="Membership lines",
        domain=[("state", "in", ["invoiced", "paid", "free"])],
    )

    def stop(self, date_end, manual_renew_needed=False, post_message=True):
        res = super().stop(date_end, manual_renew_needed, post_message)

        for rec in self:
            rec.membership_line_ids.write({"date_to": date_end})

        return res

    def _prepare_invoice_line(self, move_form):
        res = super()._prepare_invoice_line(move_form)

        # Add contract name to invoice line description
        res["name"] = f"{self.contract_id.name} / {res['name']}"

        return res