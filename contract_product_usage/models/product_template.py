from odoo import fields, models


class ProductTemplate(models.Model):

    _inherit = "product.template"

    contract_ids = fields.Many2many(
        string="Contracts",
        comodel_name="contract.contract",
        compute="_compute_contract_ids",
    )
    contract_count = fields.Integer(
        string="Contract count",
    )

    contract_line_ids = fields.Many2many(
        string="Contract lines",
        comodel_name="contract.line",
        compute="_compute_contract_ids",
    )
    contract_line_count = fields.Integer(
        string="Contract line count",
    )

    def _compute_contract_ids(self):
        for record in self:
            contract_ids = record.product_variant_ids.mapped("contract_ids")
            record.contract_ids = contract_ids
            record.contract_count = len(contract_ids)

            contract_line_ids = record.product_variant_ids.mapped("contract_line_ids")
            record.contract_line_ids = contract_line_ids
            record.contract_line_count = len(contract_line_ids)

    def action_show_contracts(self):
        self.ensure_one()
        tree_view = self.env.ref(
            "contract.contract_contract_tree_view", raise_if_not_found=False
        )
        form_view = self.env.ref(
            "contract.contract_contract_form_view", raise_if_not_found=False
        )
        ctx = dict(self.env.context)

        action = {
            "type": "ir.actions.act_window",
            "name": "Contracts",
            "res_model": "contract.contract",
            "view_mode": "tree,form",
            "domain": [("id", "in", self.contract_ids.ids)],
            "context": ctx,
        }
        if tree_view and form_view:
            action["views"] = [(tree_view.id, "tree"), (form_view.id, "form")]
        return action

    def action_show_contract_lines(self):
        self.ensure_one()
        tree_view = self.env.ref(
            "contract.contract_line_tree_view", raise_if_not_found=False
        )
        ctx = dict(self.env.context)

        action = {
            "type": "ir.actions.act_window",
            "name": "Contract lines",
            "res_model": "contract.line",
            "view_mode": "tree",
            "domain": [("id", "in", self.contract_line_ids.ids)],
            "context": ctx,
        }
        if tree_view:
            action["views"] = [(tree_view.id, "tree")]
        return action
