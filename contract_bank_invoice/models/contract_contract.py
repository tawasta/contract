from odoo import fields, models


class ContractContract(models.Model):

    _inherit = "contract.contract"

    partner_bank_id = fields.Many2one(
        "res.partner.bank", string="Recipient Bank", store=True, readonly=False
    )

    def _recurring_create_invoice(self, date_ref=False):
        moves = super()._recurring_create_invoice(date_ref=date_ref)

        if self.partner_bank_id:
            for move in moves:
                move.write({"partner_bank_id": self.partner_bank_id.id})

        return moves
