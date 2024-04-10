from odoo import http
from odoo.exceptions import AccessError, MissingError
from odoo.http import request

from odoo.addons.contract.controllers.main import PortalContract


class CustomPortalContract(PortalContract):
    @http.route(
        ["/my/contracts/<int:contract_id>"], type="http", auth="user", website=True
    )
    def portal_my_contract_detail(self, contract_id, **kw):
        try:
            contract_sudo = self._document_check_access(
                "contract.contract", contract_id
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._contract_get_page_view_values(contract_sudo, **kw)
        return request.render("contract.portal_contract_page", values)
