from odoo import api
from odoo import fields
from odoo import models


class ContractLine(models.Model):
    _inherit = "contract.line"

    recurring_interval = fields.Integer(
        default=lambda self: self._get_default_recurring_interval()
    )

    recurring_rule_type = fields.Selection(
        default=lambda self: self._get_default_recurring_rule_type()
    )

    @api.model
    def _get_default_recurring_rule_type(self):
        try:
            value = self.env["ir.config_parameter"].get_param(
                "contract_line.recurring_rule_type"
            )
        except ValueError:
            value = False
        return value

    @api.model
    def _get_default_recurring_interval(self):
        try:
            value = self.env["ir.config_parameter"].get_param(
                "contract_line.recurring_interval"
            )
        except ValueError:
            value = False
        return value
