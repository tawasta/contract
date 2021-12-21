from odoo import models, _


class ContractLine(models.Model):

    _inherit = "contract.line"

    def stop(self, date_end, manual_renew_needed=False, post_message=True):
        contracts = super().stop(date_end, manual_renew_needed=False, post_message=True)
        odoobot = self.env.ref('base.partner_root')
        body = _('Contract line "%s" is stopped by contract.', self.id)
        self.contract_id.message_post(body=body, author_id=odoobot.id)

        return contracts

    def change_product_variant(
        self, contract_id=None, new_product_id=None, contract_line=None
    ):
        line = super().change_product_variant(contract_id=None, new_product_id=None, contract_line=None)
        odoobot = self.env.ref('base.partner_root')
        body = _('Contract line "%s" has been updated by contract.', self.id)
        self.contract_id.message_post(body=body, author_id=odoobot.id)

        return line
