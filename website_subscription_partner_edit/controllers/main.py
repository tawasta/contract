from odoo import http, _
from odoo.http import request
import json


class PartnerEditController(http.Controller):
    @http.route("/update_customer/<int:partner_id>", type="http", auth="user", website=True, methods=["POST"])
    def update_customer(self, partner_id, **post):
        response = {"error": False, "msg": "Customer information updated successfully!"}
        
        try:
            partner = request.env["res.partner"].browse(partner_id)
            
            if not partner:
                response.update({"error": True, "msg": "Customer not found."})
                return json.dumps(response)
            
            valid_fields = request.env["res.partner"]._fields.keys()
            update_data = {key: value for key, value in post.items() if key in valid_fields and value}
            
            if update_data:
                partner.sudo().write(update_data)
            
        except Exception as e:
            response.update({"error": True, "msg": f"An error occurred: {str(e)}"})
        
        return json.dumps(response)

    @http.route(
        ["/partner/<int:partner_id>/upgrade/modal"],
        type="json",
        auth="user",
        website=True,
    )
    def get_partner_upgrade_modal(self, partner_id):
        user_partner_id = request.env["res.partner"].browse(partner_id)
        if not user_partner_id:
            return False

        return request.env["ir.ui.view"]._render_template(
            "website_subscription_partner_edit.portal_edit_customer_modal",
            {
                "user_partner_id": user_partner_id,
            },
        )
