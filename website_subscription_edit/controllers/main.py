from odoo import http, _
from odoo.http import request
import json


class SubscriptionController(http.Controller):
    @http.route(
        ["/subscription/line/<int:line_id>/upgrade"],
        type="http",
        auth="user",
        website=True,
        methods=["POST"],
    )
    def upgrade_subscription_line(self, line_id, **post):
        response = {"error": False, "msg": _("Subscription updated successfully!")}

        try:
            line = request.env["sale.subscription.line"].browse(line_id)
            if not line:
                response.update(
                    {"error": True, "msg": _("Subscription line not found.")}
                )
                return json.dumps(response)

            new_product_id = int(post.get("new_product", 0))
            if not new_product_id:
                response.update({"error": True, "msg": _("No new product selected.")})
                return json.dumps(response)

            subscription = line.sale_subscription_id
            if not subscription:
                response.update(
                    {"error": True, "msg": _("No subscription found for this line.")}
                )
                return json.dumps(response)

            line.action_stop()

            new_line_vals = {
                "sale_subscription_id": subscription.id,
                "date_start": subscription.recurring_next_date,
                "product_id": new_product_id,
                "product_uom_qty": line.product_uom_qty,
                "price_unit": request.env["product.product"]
                .browse(new_product_id)
                .lst_price,
            }

            if hasattr(line, "partner_id"):
                new_line_vals["partner_id"] = line.partner_id.id

            new_line = (
                request.env["sale.subscription.line"].sudo().create(new_line_vals)
            )
            new_line.action_start(immediate=False)

        except Exception:
            response.update(
                {
                    "error": True,
                    "msg": _(
                        "An error occurred while upgrading the subscription line."
                    ),
                }
            )

        return json.dumps(response)

    @http.route(
        ["/subscription/line/<int:line_id>/upgrade/modal"],
        type="json",
        auth="user",
        website=True,
    )
    def get_upgrade_modal(self, line_id):
        line = request.env["sale.subscription.line"].browse(line_id)
        if not line:
            return False

        line_product_id = line.product_id

        products = (
            request.env["product.template"]
            .sudo()
            .search(
                [
                    ("id", "=", line_product_id.product_tmpl_id.id),
                    ("subscription_change_allowed", "=", True),
                ]
            )
            .mapped("product_variant_ids")
        )

        return request.env["ir.ui.view"]._render_template(
            "website_subscription_edit.subscription_line_upgrade_modal",
            {
                "line": line,
                "products": products,
            },
        )
