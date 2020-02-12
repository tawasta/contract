from odoo import api, models


class Contract(models.Model):
    _inherit = "contract.contract"

    @api.multi
    def _prepare_sale(self, *args, **kwargs):
        # Super will handle ensure_one() and other validation
        res = super(Contract, self)._prepare_sale(*args, **kwargs)

        # Add salesperson to writable values
        if self.user_id:
            res["user_id"] = self.user_id.id

        return res

    @api.multi
    def _prepare_invoice(self, *args, **kwargs):
        # Super will handle ensure_one() and other validation
        res = super(Contract, self)._prepare_invoice(*args, **kwargs)

        # Add salesperson to writable values
        if self.user_id:
            res["user_id"] = self.user_id.id

        return res
