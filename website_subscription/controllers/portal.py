import json
from odoo import http
from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal


class PortalSubscription(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if "subscription_count" in counters:
            subscription_model = request.env["sale.subscription"]
            subscription_count = (
                subscription_model.search_count([])
                if subscription_model.check_access_rights("read", raise_exception=False)
                else 0
            )
            values["subscription_count"] = subscription_count
        return values

    @http.route(
        ["/my/subscriptions"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_subscriptions(self, **kw):
        values = self._prepare_portal_layout_values()
        subscription_obj = request.env["sale.subscription"]
        # Avoid error if the user does not have access.
        if not subscription_obj.check_access_rights("read", raise_exception=False):
            return request.redirect("/my")

        subscriptions = (
            request.env["sale.subscription"]
            .sudo()
            .search([("partner_id", "=", request.env.user.partner_id.id)])
        )
        values.update(
            {
                "subscriptions": subscriptions,
                "page_name": "Subscriptions",
                "default_url": "/my/subscriptions",
            }
        )
        return request.render("website_subscription.portal_my_subscriptions", values)

    @http.route(
        ["/my/subscriptions/<int:subscription_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_subscription_detail(self, subscription_id, **kw):
        subscription = request.env["sale.subscription"].browse(subscription_id)
        values = {"subscription": subscription}
        return request.render("website_subscription.portal_subscription_page", values)

    # Otetaan myöhemmin käyttöön
    # @http.route(
    #     ["/subscription/cancel/<int:subscription_id>"],
    #     type="http",
    #     auth="user",
    #     website=True,
    #     csrf=False,
    # )
    # def cancel_subscription(self, subscription_id=None, **post):
    #     subscription = (
    #         request.env["sale.subscription"]
    #         .sudo()
    #         .search([("id", "=", subscription_id)])
    #     )
    #     closed_stage = request.env["sale.subscription.stage"].search(
    #         [("type", "=", "post")], limit=1
    #     )

    #     subscription.sudo().write({"stage_id": closed_stage.id})

    #     subscription.active = False

    #     values = {}
    #     return json.dumps(values)
