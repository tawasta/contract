from odoo import _, http
from odoo.exceptions import AccessError
from odoo.http import content_disposition, request

from odoo.addons.portal.controllers.portal import CustomerPortal


class MemberCertificateCustomerPortal(CustomerPortal):
    def _prepare_portal_layout_values(self):
        """Check if the printing option should be shown in the sidebar"""
        values = super()._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        values["can_print_member_certificate"] = partner._can_print_member_certificate()
        return values

    def _check_member_certificate_access(self, partner):
        """Overridable access guard. Raises AccessError if the current portal
        user may not print this partner's certificate."""
        if not partner or partner != request.env.user.partner_id:
            raise AccessError(_("You can only print your own membership certificate."))
        if not partner._can_print_member_certificate():
            raise AccessError(
                _("Membership certificate printing is not possible for your account.")
            )

    @http.route(
        ["/my/membership-certificate"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_print_member_certificate(self, **kw):
        partner = request.env.user.partner_id
        self._check_member_certificate_access(partner)

        pdf_content, _content_type = (
            request.env["ir.actions.report"]
            .sudo()
            ._render_qweb_pdf(
                "partner_member_certificate_report.action_pdf_cert_report",
                partner.ids,
            )
        )
        filename = _("%s - Membership Certificate.pdf") % (
            partner.name or _("Certificate")
        )
        return request.make_response(
            pdf_content,
            headers=[
                ("Content-Type", "application/pdf"),
                ("Content-Length", len(pdf_content)),
                ("Content-Disposition", content_disposition(filename)),
            ],
        )
