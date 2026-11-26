from werkzeug.exceptions import Forbidden

from odoo import http
from odoo.http import request

# The reference goes to the invoice reference, which a Finvoice e-invoice
# carries in a field of at most 70 characters
INVOICE_REF_MAX_LENGTH = 70


class SubscriptionCustomerReference(http.Controller):
    @http.route(
        "/my/subscriptions/<int:subscription_id>/invoice_ref",
        type="http",
        auth="user",
        website=True,
        methods=["POST"],
    )
    def update_invoice_ref(self, subscription_id, invoice_ref="", **post):
        """Save the customer reference of the user's own subscription and
        return to the subscription page with the result."""
        # A search applies the record rules without an access error, so a
        # missing and another customer's subscription get the same answer
        subscription = request.env["sale.subscription"].search(
            [("id", "=", subscription_id)], limit=1
        )
        if not subscription or not subscription._portal_can_edit_invoice_ref():
            raise Forbidden()

        invoice_ref = invoice_ref.strip()
        status = self._check_invoice_ref(invoice_ref)
        if status == "saved":
            # sudo: access is decided by _portal_can_edit_invoice_ref() above,
            # not by the portal write rule, which also covers followers. Only
            # this field is written, and the change is tracked in the name of
            # the user, as sudo keeps the user.
            subscription.sudo().write({"invoice_ref": invoice_ref})
        return request.redirect(
            f"/my/subscriptions/{subscription.id}?invoice_ref_status={status}"
        )

    def _check_invoice_ref(self, invoice_ref):
        if not invoice_ref:
            return "empty"
        if len(invoice_ref) > INVOICE_REF_MAX_LENGTH:
            return "too_long"
        return "saved"
