from datetime import date

from odoo import api, fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    @api.depends(
        "member_lines.account_invoice_line",
        "member_lines.account_invoice_line.move_id.state",
        "member_lines.account_invoice_line.move_id.payment_state",
        "member_lines.account_invoice_line.move_id.partner_id",
        "free_member",
        "member_lines.date_to",
        "member_lines.date_from",
        "associate_member",
    )
    def _compute_membership_state(self):
        """
        Override to allow using contract partner instead of invoice partner
        """
        res = super()._compute_membership_state()
        today = fields.Date.today()

        for partner in self:
            state = "none"

            partner.membership_start = (
                self.env["membership.membership_line"]
                .search(
                    [
                        ("partner", "=", partner.associate_member.id or partner.id),
                        ("date_cancel", "=", False),
                    ],
                    limit=1,
                    order="date_from",
                )
                .date_from
            )
            partner.membership_stop = (
                self.env["membership.membership_line"]
                .search(
                    [
                        ("partner", "=", partner.associate_member.id or partner.id),
                        ("date_cancel", "=", False),
                    ],
                    limit=1,
                    order="date_to desc",
                )
                .date_to
            )
            partner.membership_cancel = (
                self.env["membership.membership_line"]
                .search([("partner", "=", partner.id)], limit=1, order="date_cancel")
                .date_cancel
            )

            if partner.membership_cancel and today > partner.membership_cancel:
                partner.membership_state = "free" if partner.free_member else "canceled"
                continue
            if partner.membership_stop and today > partner.membership_stop:
                if partner.free_member:
                    partner.membership_state = "free"
                    continue
            if partner.associate_member:
                partner.associate_member._compute_membership_state()
                partner.membership_state = partner.associate_member.membership_state
                continue

            # This is the only changed thing
            line_states = [
                mline.state
                for mline in partner.member_lines
                if (mline.date_to or date.min) >= today >= (mline.date_from or date.min)
                and mline.account_invoice_line.move_id.partner_id == partner
                or (
                    mline.contract_line_id
                    and mline.contract_line_id.partner_id == partner
                )
            ]

            if "paid" in line_states:
                state = "paid"
            elif "invoiced" in line_states:
                state = "invoiced"
            elif "waiting" in line_states:
                state = "waiting"
            elif "canceled" in line_states:
                state = "canceled"

            if state == "none":
                for mline in partner.member_lines:
                    # if there is an old invoice paid, set the state to 'old'
                    if (
                        (mline.date_from or date.min) < today
                        and today
                        > (mline.date_to or date.min)
                        >= (mline.date_from or date.min)
                        and mline.account_invoice_id
                        and mline.account_invoice_id.payment_state
                        in ("in_payment", "paid")
                    ):
                        state = "old"
                        break

            if partner.free_member and state != "paid":
                state = "free"
            partner.membership_state = state

        return res
