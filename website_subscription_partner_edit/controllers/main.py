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
                existing_contact = request.env["res.partner"].browse(
                    int(post["existing_contact"])
                )
                if existing_contact.exists():
                    subscription.write({"partner_id": existing_contact.id})

                else:
                    response.update(
                        {"error": True, "msg": "Selected contact not found."}
                    )
                    return json.dumps(response)

            else:
                # Creating a new contact
                new_contact_vals = {
                    key: post.get(key)
                    for key in [
                        "email",
                        "phone",
                        "street",
                        "zip",
                        "city",
                    ]
                }
                new_contact_vals["type"] = "invoice"
                new_contact_vals["parent_id"] = partner.id

                is_company = post.get("is_company") == "on"

                if is_company:
                    new_contact_vals["is_company"] = True
                    new_contact_vals["name"] = post.get("name")
                    if post.get("company_registry"):
                        new_contact_vals["company_registry"] = post.get(
                            "company_registry"
                        )
                else:
                    firstname = post.get("firstname") or ""
                    lastname = post.get("lastname") or ""
                    new_contact_vals["firstname"] = firstname
                    new_contact_vals["lastname"] = lastname

                # Country & Transmit Method
                transmit_method_id = post.get("customer_invoice_transmit_method_id")
                if transmit_method_id:
                    new_contact_vals["customer_invoice_transmit_method_id"] = int(
                        transmit_method_id
                    )

                    # Fetch transmit method code
                    method = (
                        request.env["transmit.method"]
                        .sudo()
                        .browse(int(transmit_method_id))
                    )
                    if method and method.code == "einvoice" and is_company:
                        # Only add these if method is 'einvoice' and customer is a company
                        if post.get("edicode"):
                            new_contact_vals["edicode"] = post.get("edicode")
                        if post.get("einvoice_operator_id"):
                            new_contact_vals["einvoice_operator_id"] = int(
                                post["einvoice_operator_id"]
                            )

                    if method.code == "ocr":
                        # Tarkistetaan, että kenttä on olemassa mallissa
                        if hasattr(
                            request.env["res.partner"], "email_invoicing_address"
                        ):
                            if post.get("email"):
                                new_contact_vals["email_invoicing_address"] = post.get(
                                    "email"
                                )

                if post.get("country_id"):
                    new_contact_vals["country_id"] = int(post["country_id"])

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
