from odoo import http, _
from odoo.http import request
import json


class PartnerEditController(http.Controller):
    @http.route(
        "/update_customer/<int:partner_id>/subscription/<int:subscription_id>",
        type="http",
        auth="user",
        website=True,
        methods=["POST"],
    )
    def update_customer(self, partner_id, subscription_id, **post):
        response = {"error": False, "msg": "Customer information updated successfully!"}

        try:
            partner = request.env["res.partner"].browse(partner_id)
            subscription = request.env["sale.subscription"].browse(subscription_id)

            if not partner.exists():
                response.update({"error": True, "msg": "Customer not found."})
                return json.dumps(response)
            if not subscription.exists():
                response.update({"error": True, "msg": "Subscription not found."})
                return json.dumps(response)

            if post.get("existing_contact"):
                # Käyttäjä valitsi olemassa olevan kontaktin
                existing_contact = request.env["res.partner"].browse(
                    int(post["existing_contact"])
                )
                if existing_contact.exists():
                    subscription.write({"partner_id": existing_contact.id})

                else:
                    response.update({"error": True, "msg": "Selected contact not found."})
                    return json.dumps(response)

            else:
                # Käyttäjä luo uuden kontaktin
                new_contact_vals = {
                    "name": f"{post.get('firstname', '')} {post.get('lastname', '')}",
                    "email": post.get("email"),
                    "phone": post.get("phone"),
                    "street": post.get("street"),
                    "parent_id": partner.id,  # Liitetään pääkontaktiin
                }
                new_contact = request.env["res.partner"].sudo().create(new_contact_vals)
                partner.write({"child_ids": [(4, new_contact.id)]})
                subscription.write({"partner_id": new_contact.id})

        except Exception as e:
            response.update({"error": True, "msg": f"An error occurred: {str(e)}"})

        return json.dumps(response)

    @http.route(
        ["/partner/<int:partner_id>/subscription/<int:subscription_id>/upgrade/modal"],
        type="json",
        auth="user",
        website=True,
    )
    def get_partner_upgrade_modal(self, partner_id, subscription_id):
        user_partner = request.env["res.partner"].browse(partner_id)
        subscription = request.env["sale.subscription"].browse(subscription_id)

        if not user_partner.exists() or not subscription.exists():
            return False

        # Hakee kaikki kontaktit ilman user_partner_id:tä
        contacts = user_partner.child_ids
        if user_partner.commercial_partner_id:
            commercial_partner = user_partner.commercial_partner_id
            contacts |= commercial_partner.child_ids | commercial_partner

        # Poistaa duplikaatit ja varmistaa, ettei user_partner_id ole listalla
        unique_contacts = request.env["res.partner"].browse(
            list(set(contacts.ids) - {user_partner.id})
        )

        return request.env["ir.ui.view"]._render_template(
            "website_subscription_partner_edit.portal_edit_customer_modal",
            {
                "user_partner_id": user_partner,
                "subscription": subscription,
                "contacts": unique_contacts,  # Lopullinen lista ilman user_partner_id:tä
            },
        )

