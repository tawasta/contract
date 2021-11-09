# 1. Standard library imports:
import json
from datetime import date, datetime

from odoo import http
from odoo.http import request

# 2. Known third party imports:
# 3. Odoo imports (openerp):


class UpgradeContractLine(http.Controller):
    @http.route(
        ["/contract/get/<int:line_id>"],
        type="http",
        auth="user",
        website=True,
        csrf=False,
    )
    def get_line_data(self, line_id=None, **post):
        """
        Get contract line data with AJAX.

        :param line_id: Contract line ID
        :return: JSON
        """
        current_user = request.env.user

        current_line = request.env["contract.line"].search([("id", "=", line_id)])
        products = current_line.product_id.product_tmpl_id.product_variant_ids
        values = {"current_line": current_line, "products": products}
        line_html = ""
        if current_line:
            line_html = request.render(
                "website_upgrade_contract_line.upgrade_line", values, lazy=False
            ).decode("UTF-8")

        line_values = {"line_html": line_html}
        return json.dumps(line_values)

    @http.route(
        ["/contract/line/upgrade"], type="http", auth="user", website=True, csrf=False
    )
    def upgrade_contract_line(self, **post):
        line = (
            request.env["contract.line"]
            .sudo()
            .search([("id", "=", post.get("upgrade_line_id"))])
        )
        redirect_url = post.get("return_url")
        product = (
            request.env["product.product"]
            .sudo()
            .search([("id", "=", post.get("product_id"))])
        )
        updateline = request.env["contract.line"].change_product_variant(
            line.contract_id, product, line
        )

        return request.redirect(redirect_url)
