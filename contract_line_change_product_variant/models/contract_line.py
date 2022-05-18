from odoo import api, fields, models


class ContractLine(models.Model):

    _inherit = "contract.line"

    ignore_recurring_next_date = fields.Boolean(default=False)

    @api.constrains("recurring_next_date", "date_start")
    def _check_recurring_next_date_start_date(self):
        for line in self:
            if line.ignore_recurring_next_date:
                continue
            else:
                super(ContractLine, line)._check_recurring_next_date_start_date()

    def change_product_variant(
        self, contract_id=None, new_product_id=None, contract_line=None
    ):
        """This function is callable inside other models."""
        if contract_id and new_product_id and contract_line:
            self.env["contract.line.change.product.variant"].change_product_variant(
                contract_id=contract_id,
                new_product_id=new_product_id,
                contract_line=contract_line,
            )
        return True

    def change_product_variant_wizard(self):
        product = self.product_id
        contract_line = self.id
        contract_id = self.contract_id.id
        # available_variants = product.product_tmpl_id.product_variant_ids
        available_variants = (
            self.env["product.template"]
            .sudo()
            .search(
                [("id", "=", product.product_tmpl_id.id), ("change_allowed", "=", True)]
            )
            .mapped("product_variant_ids")
        )
        view_id = self.env.ref(
            "contract_line_change_product_variant."
            "contract_line_change_product_variant_wizard"
        ).id
        wiz = (
            self.env["contract.line.change.product.variant"]
            .sudo()
            .create(
                {
                    "old_product_id": product.id,
                    "product_id": product.id,
                    "contract_line": contract_line,
                    "contract_id": contract_id,
                    "available_variants": available_variants,
                }
            )
        )

        return {
            "name": "Change member product",
            "view_mode": "form",
            "res_model": "contract.line.change.product.variant",
            "view_id": view_id,
            "type": "ir.actions.act_window",
            "res_id": wiz.id,
            "target": "new",
        }
