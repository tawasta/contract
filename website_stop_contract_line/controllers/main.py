# 1. Standard library imports:
import json
from datetime import date, datetime

from odoo import http
from odoo.http import request

# 2. Known third party imports:
# 3. Odoo imports (openerp):


class StopContractLine(http.Controller):
    @http.route(
        ["/contract/line/stop/<int:line_id>"],
        type="http",
        auth="user",
        website=True,
        csrf=False,
    )
    def stop_contract_line(self, line_id=None, **post):
        line = request.env["contract.line"].sudo().search([("id", "=", line_id)])
        line.sudo().stop(date.today(), manual_renew_needed=False)
        values = {}
        return json.dumps(values)
