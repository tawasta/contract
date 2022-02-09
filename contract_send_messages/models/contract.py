from odoo import api, models


class ContractContract(models.Model):

    _inherit = "contract.contract"

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        partners = self.env["website"].get_current_website().contract_email_ids
        if partners:
            for rec in records:
                rec.message_subscribe(partner_ids=partners.ids)

        return records
