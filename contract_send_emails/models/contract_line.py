from odoo import fields, models


class ContractLine(models.Model):

    _inherit = "contract.line"

    def stop(self, date_end, manual_renew_needed=False, post_message=True):
        # Super will handle ensure_one() and other validation
        contracts = super().stop(date_end, manual_renew_needed=False, post_message=True)
        print(contracts)
        print(self)
