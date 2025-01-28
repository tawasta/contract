import json
import secrets
from collections import defaultdict
from datetime import datetime

import werkzeug
from werkzeug.exceptions import Forbidden

from odoo import _, http
from odoo.http import request


class SubscriptionInviteController(http.Controller):

    @http.route(
        ["/send/invitation"],
        type="http",
        auth="user",
        website=True,
        csrf=False,
    )
    def send_invitation(self, **post):
        line_id = post.get("line_id")
        if not line_id:
            return json.dumps(
                {"status": "error", "message": "Subscription line ID is missing"}
            )

        subscription_line = (
            request.env["sale.subscription.line"]
            .sudo()
            .search([("id", "=", int(line_id))], limit=1)
        )

        if not subscription_line:
            return json.dumps({"status": "error", "message": "Subscription line not found"})

        invite_email = post.get("invite_email")
        if not invite_email:
            return json.dumps({"status": "error", "message": "No email provided"})

        if post.get("invite_id"):
            old_invite_id = (
                request.env["subscription.invitation"]
                .sudo()
                .search([("id", "=", int(post.get("invite_id")))], limit=1)
            )

            if old_invite_id and old_invite_id == subscription_line.invite_id:
                old_invite_id.unlink()

        invite_tracker = (
            request.env["subscription.invitation"]
            .sudo()
            .create(
                {
                    "subscription_id": subscription_line.id,
                    "invite_email": invite_email,
                    "invited_date": datetime.now(),
                    "is_used": False,
                    "access_token": secrets.token_urlsafe(32),
                }
            )
        )

        subscription_line.sudo().write({"invite_id": invite_tracker.id})

        mail_template = request.env.ref(
            "subscription_invite.subscription_invitation_email_template"
        ).sudo()
        if not mail_template:
            return json.dumps(
                {"status": "error", "message": "Email template not found"}
            )

        email_values = {
            "email_to": invite_email,
            "auto_delete": True,
            "message_type": "email",
            "recipient_ids": [],
            "partner_ids": [],
        }

        try:
            mail_template.send_mail(
                subscription_line.id,
                force_send=True,
                raise_exception=True,
                email_values=email_values,
            )
            body = f"An invitation has been sent to the email address: {invite_email}."

        except Exception as e:
            return json.dumps(
                {"status": "error", "message": f"Failed to send invitation: {str(e)}"}
            )

        return json.dumps(
            {
                "status": "success",
                "message": _("Invitation sent"),
                "invite_id": invite_tracker.id,
            }
        )

    @http.route(
        ["/invitation/<int:invite_id>/accept"],
        type="http",
        auth="user",
        website=True,
    )
    def accept_invitation(self, invite_id, access_token=None, **post):
        invitation = (
            request.env["subscription.invitation"]
            .sudo()
            .search([("id", "=", invite_id)], limit=1)
        )

        if not invitation or invitation.access_token != access_token:
            raise Forbidden()

        if request.env.user.partner_id.email != invitation.invite_email:
            raise Forbidden()

        if invitation.is_used:
            values = {
                "invitation": invitation,
                "show_thank_you": True,
            }
            return request.render(
                "subscription_invite.subscription_invitation_form", values
            )

        values = {
            "invitation": invitation,
            "counter": 1,
        }

        return request.render(
            "subscription_invite.subscription_invitation_form", values
        )

    # # flake8: noqa: C901
    @http.route(
        ["/accept_subscription_invitation"], type="http", auth="user", website=True, csrf=True
    )
    def accept_invitation_form(self, **post):
        invite_data = {
            "invite_id": post.pop("invite_id", None),
            "access_token": post.pop("access_token", None),
            "subscription_id": post.pop("subscription_id", None),
            "return_url": post.pop("return_url", None),
        }

        invitation = (
            request.env["subscription.invitation"]
            .sudo()
            .search([("id", "=", invite_data["invite_id"])], limit=1)
        )

        invitation.sudo().write(
            {
                "is_used": True,
                "used_date": datetime.now(),
            }
        )

        invitation.subscription_id.sudo().write({"partner_id": request.env.user.partner_id.id})


        return_url = f"{invite_data['return_url']}?access_token={invite_data['access_token']}&thank_you=1"

        return request.redirect(return_url)
