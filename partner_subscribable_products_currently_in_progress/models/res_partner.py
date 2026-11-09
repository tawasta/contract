from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    subscribable_product_ids_in_progress = fields.Many2many(
        comodel_name="product.product",
        relation="res_partner_subscribable_product_in_progress_rel",
        string="Products in Currently Ongoing Subscription Lines",
        compute="_compute_subscribable_product_ids_in_progress",
        store=True,
        readonly=True,
        help="Products on this partner's subscription lines whose subscription "
        "is in progress. Refreshed automatically when subscription lines or "
        "subscriptions change.",
    )

    show_subscribable_products_in_progress_page = fields.Boolean(
        compute="_compute_show_subscribable_products_in_progress_page",
    )

    @api.depends(
        "subscription_line_ids",
        "subscription_line_ids.product_id",
        "subscription_line_ids.sale_subscription_id",
        "subscription_line_ids.sale_subscription_id.in_progress",
    )
    def _compute_subscribable_product_ids_in_progress(self):
        for partner in self:
            lines_in_progress = partner.sudo().subscription_line_ids.filtered(
                lambda line: line.sale_subscription_id.in_progress
            )
            partner.subscribable_product_ids_in_progress = lines_in_progress.product_id

    def _compute_show_subscribable_products_in_progress_page(self):
        show = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param(
                "partner_subscribable_products_currently_in_progress.show_partner_page",
                "True",
            )
            == "True"
        )
        for partner in self:
            partner.show_subscribable_products_in_progress_page = show

    def action_view_subscription_lines_in_progress(self):
        """Launch the subscription line listview"""
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "subscription_line_list_view.action_subscription_lines"
        )
        action.update(
            {
                "name": self.display_name,
                "domain": [("partner_id", "=", self.id)],
                "context": {"default_partner_id": self.id},
            }
        )
        return action
