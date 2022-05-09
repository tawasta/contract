from odoo import models


class ContractContract(models.Model):

    _inherit = "contract.contract"

    def _prepare_invoice(self, *args, **kwargs):
        res = super()._prepare_invoice(*args, **kwargs)
        comment = res.get("comment", "")
        if self.note:
            res["comment"] = "{}{}{}".format(
                self.note, "\n" if comment else "", comment
            )
        return res
