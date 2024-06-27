from odoo import api, fields, models


class Contract(models.Model):
    _inherit = "contract.contract"

    line_partner_count = fields.Integer(compute="_compute_line_partner_count")

    def _compute_line_partner_count(self):
        for rec in self:
            partners = rec._get_related_line_partners()
            rec.line_partner_count = len(partners)

    def _get_related_line_partners(self):
        self.ensure_one()
        return self.contract_line_ids.mapped("partner_id")

    def action_show_line_partners(self):
        self.ensure_one()
        tree_view = self.env.ref("base.view_partner_tree", raise_if_not_found=False)
        form_view = self.env.ref("base.view_partner_form", raise_if_not_found=False)
        ctx = dict(self.env.context)

        action = {
            "type": "ir.actions.act_window",
            "name": "Partners",
            "res_model": "res.partner",
            "view_mode": "tree,kanban,form",
            "domain": [("id", "in", self._get_related_line_partners().ids)],
            "context": ctx,
        }
        if tree_view and form_view:
            action["views"] = [(tree_view.id, "tree"), (form_view.id, "form")]
        return action
