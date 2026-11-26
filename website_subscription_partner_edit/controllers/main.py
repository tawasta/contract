import json
import logging

from werkzeug.exceptions import Forbidden

from odoo import _, http, tools
from odoo.exceptions import ValidationError
from odoo.http import request

_logger = logging.getLogger(__name__)


class PartnerEditController(http.Controller):
    @http.route(
        "/update_customer/<int:partner_id>/subscription/<int:subscription_id>",
        type="http",
        auth="user",
        website=True,
        methods=["POST"],
    )
    def update_customer(self, partner_id, subscription_id, **post):
        """
        Updates the customer of the subscription or creates a new contact for it.
        NOTE! The partner of the logged-in user is always the main partner,
        so that new contacts are linked to the right customer.
        """
        response = {
            "error": False,
            "msg": _("Customer information updated successfully!"),
        }

        try:
            # The partner of the logged-in user is always the main partner
            partner = request.env.user.partner_id
            subscription = self._get_subscription(subscription_id)

            if not partner.exists():
                response.update({"error": True, "msg": "Customer not found."})
                return json.dumps(response)
            if not subscription.exists():
                response.update({"error": True, "msg": "Subscription not found."})
                return json.dumps(response)

            if post.get("edit_contact_id"):
                # The user edited an existing invoice address
                contact = self._edit_invoice_address(
                    subscription, int(post["edit_contact_id"]), post
                )
                subscription.write({"partner_id": contact.id})

            elif post.get("existing_contact"):
                # The user selected an existing contact
                existing_contact = request.env["res.partner"].browse(
                    int(post["existing_contact"])
                )
                # Only a contact of the selection, never any ID from the browser
                selectable = (
                    self._get_invoice_contacts(subscription) | subscription.partner_id
                )
                if existing_contact in selectable:
                    subscription.write({"partner_id": existing_contact.id})

                else:
                    response.update(
                        {"error": True, "msg": "Selected contact not found."}
                    )
                    return json.dumps(response)

            else:
                # Create a new contact
                is_company = post.get("is_company") == "on"
                new_contact_vals = self._prepare_contact_values(post, is_company)
                new_contact_vals.update(
                    {
                        "type": "invoice",
                        # An invoice address of a company or of a person
                        "is_company": is_company,
                        # Linked on create: a portal user cannot write the own
                        # partner, which the former child_ids write needed
                        "parent_id": partner.id,
                    }
                )
                self._validate_contact_values(new_contact_vals, is_company)
                new_contact = request.env["res.partner"].sudo().create(new_contact_vals)
                subscription.write({"partner_id": new_contact.id})

        # Only the checks of the form are shown to the user: the text of any
        # other error could reveal data of the database
        except ValidationError as error:
            # A constraint may fail after a write: nothing of the request is kept
            request.env.cr.rollback()
            response.update({"error": True, "msg": error.args[0]})

        return json.dumps(response)

    @http.route(
        ["/partner/<int:partner_id>/subscription/<int:subscription_id>/upgrade/modal"],
        type="json",
        auth="user",
        website=True,
    )
    def get_partner_upgrade_modal(self, partner_id, subscription_id):
        """
        Returns the modal for choosing the invoice address (partner) of the
        subscription.
        Special case: when the partner has a parent_id that is the partner of
        the logged-in user, it is an invoice address of the company type.
        Then all the contacts of the parent and the parent itself are included.
        """
        # The current invoice address comes from the subscription, not from
        # the partner_id of the route, which the browser could change
        subscription = self._get_subscription(subscription_id)
        user_partner = subscription.partner_id

        if not user_partner.exists() or not subscription.exists():
            return False

        unique_contacts = self._get_invoice_contacts(subscription)

        # The settings of the website: the marking of the current address
        # and the editing of the addresses
        website = request.website
        current_contact = user_partner
        editable_contacts = self._get_editable_contacts(
            subscription, unique_contacts | user_partner
        )
        if website.subscription_show_current_invoice_address:
            unique_contacts = current_contact | unique_contacts
        else:
            if current_contact in editable_contacts:
                # Listed without the marking, so that it can be edited
                unique_contacts |= current_contact
            current_contact = current_contact.browse()

        return request.env["ir.ui.view"]._render_template(
            "website_subscription_partner_edit.portal_edit_customer_modal",
            {
                "user_partner_id": user_partner,
                "subscription": subscription,
                # Final list without user_partner_id
                "contacts": unique_contacts,
                "current_contact": current_contact,
                # With both settings off the cards look as before
                "show_full_address": website.subscription_show_current_invoice_address
                or website.subscription_edit_invoice_address,
                "editable_contacts": editable_contacts,
                **self._prepare_address_form_values(request.env["res.partner"]),
            },
        )

    @http.route(
        "/my/subscriptions/<int:subscription_id>/invoice_address/<int:contact_id>/form",
        type="json",
        auth="user",
        website=True,
    )
    def get_invoice_address_form(self, subscription_id, contact_id):
        """Render the form for editing an existing invoice address."""
        subscription = self._get_subscription(subscription_id)
        contact = self._get_editable_contacts(subscription).filtered(
            lambda editable: editable.id == contact_id
        )
        if not contact:
            raise Forbidden()
        return request.env["ir.ui.view"]._render_template(
            "website_subscription_partner_edit.portal_invoice_address_form",
            self._prepare_address_form_values(contact),
        )

    def _get_subscription(self, subscription_id):
        """The subscription, when it is billed to the user's own contacts,
        else an empty recordset. One search, so that a missing subscription
        and another customer's look the same. The ownership is checked here,
        as the portal record rule also shows a subscription to its followers."""
        commercial_partner = request.env.user.commercial_partner_id
        return request.env["sale.subscription"].search(
            [
                ("id", "=", subscription_id),
                ("partner_id", "child_of", commercial_partner.id),
            ],
            limit=1,
        )

    def _get_invoice_contacts(self, subscription):
        """The contacts the subscription can be billed to, as the module has
        always listed them."""
        user_partner = subscription.partner_id

        # All partners related to users partner
        contacts = user_partner.child_ids

        # Special case:
        # billing address (company type) linked to the logged-in user's partner

        # If this condition is met,
        # also fetch all contacts of the parent and the parent itself
        if (
            user_partner.parent_id
            and user_partner.parent_id == request.env.user.partner_id
        ):
            contacts |= user_partner.parent_id.child_ids | user_partner.parent_id

        if user_partner.commercial_partner_id:
            commercial_partner = user_partner.commercial_partner_id
            contacts |= commercial_partner.child_ids | commercial_partner

        # Removes duplicates and ensures user_partner_id is not in the list
        return request.env["res.partner"].browse(
            list(set(contacts.ids) - {user_partner.id})
        )

    def _get_editable_contacts(self, subscription, invoice_contacts=None):
        """Addresses the user can edit, as in the checkout: their own contact
        and the invoice and other addresses, not the commercial entity."""
        if not request.website.subscription_edit_invoice_address:
            return request.env["res.partner"]
        if invoice_contacts is None:
            invoice_contacts = (
                self._get_invoice_contacts(subscription) | subscription.partner_id
            )
        user_partner = request.env.user.partner_id
        return invoice_contacts.filtered(
            lambda contact: contact == user_partner
            or contact.type in ("invoice", "other")
        )

    def _edit_invoice_address(self, subscription, contact_id, post):
        """Save an edited invoice address with the restrictions of the
        checkout. The form shows the locked fields read-only, so a change of
        one comes only from a hand-crafted request."""
        contact = self._get_editable_contacts(subscription).filtered(
            lambda editable: editable.id == contact_id
        )
        if not contact:
            raise Forbidden()
        # The address keeps its current method also when the website does not
        # offer it, for example one set by the back office
        values = self._prepare_contact_values(
            post, contact.is_company, contact.customer_invoice_transmit_method_id
        )
        locked_fields = contact.sudo()._get_portal_locked_fields()
        reasons = {
            reason
            for field, reason in locked_fields.items()
            if field in values and values[field] != (contact[field] or False)
        }
        if reasons:
            raise ValidationError("\n".join(sorted(reasons)))
        values = {
            field: value
            for field, value in values.items()
            if field not in locked_fields
        }
        self._validate_contact_values(values, contact.is_company)
        # sudo: portal users cannot write contacts. The contact is one of the
        # user's own editable addresses and the values hold only the fields
        # of the form, without the locked ones.
        contact.sudo().write(values)
        return contact

    def _prepare_contact_values(self, post, is_company, current_method=None):
        """The fields of the address form, for a new and an edited address.
        An empty field is False, which clears it on an edit."""
        if is_company:
            name_fields = ["name", "company_registry"]
        else:
            name_fields = ["firstname", "lastname"]
        fields = ["email", "phone", "street", "zip", "city", *name_fields]
        values = {field: post.get(field) or False for field in fields}
        values["country_id"] = self._get_reference_id(
            "res.country", post.get("country_id")
        )
        method = self._get_transmit_method(
            post.get("customer_invoice_transmit_method_id"), is_company, current_method
        )
        if method:
            values["customer_invoice_transmit_method_id"] = method.id
            # The eInvoice fields only for a company that is invoiced by eInvoice
            if method.code == "einvoice" and is_company:
                values["edicode"] = post.get("edicode") or False
                values["einvoice_operator_id"] = self._get_reference_id(
                    "res.partner.operator.einvoice", post.get("einvoice_operator_id")
                )
            # Only when the field exists in the model
            if method.code == "ocr" and "email_invoicing_address" in (
                request.env["res.partner"]._fields
            ):
                values["email_invoicing_address"] = post.get("email") or False
        return values

    def _get_transmit_method(self, method_id, is_company, current_method=None):
        """The transmit method chosen in the form, when the form offers it
        for the contact type."""
        if not method_id:
            return request.env["transmit.method"]
        if current_method and int(method_id) == current_method.id:
            return current_method.sudo()
        # sudo: portal users cannot read transmit methods
        method = (
            request.env["transmit.method"]
            .sudo()
            .search(
                [("id", "=", int(method_id)), *self._get_method_domain(is_company)],
                limit=1,
            )
        )
        if not method:
            raise ValidationError(_("Select an invoice transmit method from the list."))
        return method

    def _get_method_domain(self, is_company):
        target_types = ["both", "company" if is_company else "person"]
        return [
            ("website_sale_ok", "=", True),
            ("contract_target_type", "in", target_types),
        ]

    def _get_reference_id(self, model, record_id):
        """ID of a country or an operator chosen in the form."""
        if not record_id:
            return False
        # sudo: countries and eInvoice operators are public reference data
        record = request.env[model].sudo().browse(int(record_id)).exists()
        if not record:
            raise ValidationError(
                _("A selected value is no longer available. Reload the page.")
            )
        return record.id

    def _validate_contact_values(self, values, is_company):
        """The checks of the checkout address form, on the server. Locked
        fields are not in the values and keep their saved value."""
        name_fields = ("name",) if is_company else ("firstname", "lastname")
        errors = []
        if any(
            field in values and not (values[field] or "").strip()
            for field in (*name_fields, "street", "zip", "city")
        ):
            errors.append(_("Some required fields are empty."))
        if values.get("email") and not tools.single_email_re.match(values["email"]):
            errors.append(_("Invalid Email! Please enter a valid email address."))
        if values.get("company_registry"):
            partner = request.env["res.partner"].new(
                {
                    "company_registry": values["company_registry"],
                    "country_id": values.get("country_id"),
                }
            )
            try:
                # Normalised first, as on save: 12345671 and FI12345671 are
                # valid forms of 1234567-1
                partner._check_company_registry()
            except ValidationError as error:
                errors.append(error.args[0])
        if errors:
            raise ValidationError("\n".join(errors))

    def _prepare_address_form_values(self, contact):
        """Values of the address form: an empty contact for a new address."""
        # sudo: portal users cannot read transmit methods and operators
        methods = (
            request.env["transmit.method"]
            .sudo()
            .search(
                self._get_method_domain(contact.is_company)
                if contact
                else [("website_sale_ok", "=", True)]
            )
        )
        # The current method stays selectable, so that saving keeps it
        methods |= contact.sudo().customer_invoice_transmit_method_id
        return {
            "form_contact": contact,
            "locked_fields": contact.sudo()._get_portal_locked_fields()
            if contact
            else {},
            "transmit_methods": methods,
            "operators": request.env["res.partner.operator.einvoice"].sudo().search([]),
            "countries": request.env["res.country"].sudo().search([]),
        }
