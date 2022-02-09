from odoo import models


class ContractLine(models.Model):
    _inherit = "contract.line"

    def action_open_line(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "contract.line",
            "view_mode": "form",
            "res_id": self.id,
            "target": "new",
            "flags": {"form": {"action_buttons": True}},
        }
