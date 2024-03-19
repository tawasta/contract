from odoo import api, models


class ContractContractTerminate(models.TransientModel):

    _inherit = "contract.contract.terminate"

    @api.model
    def default_get(self, fields):
        """
        Fetch and suggest default contract termination reason
        """

        res = super(ContractContractTerminate, self).default_get(fields)

        active_contract = self.env["contract.contract"].search(
            [("id", "=", self.env.context.get("active_id"))], limit=1
        )

        res[
            "terminate_reason_id"
        ] = active_contract.company_id.default_contract_terminate_reason_id.id

        return res
