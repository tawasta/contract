from odoo import _, models

NAME_FIELDS = ("name", "firstname", "lastname")


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _get_portal_locked_fields(self):
        """Return {field name: reason} for the fields a portal user cannot
        change on this address. Follows the rules of the checkout address
        form, so an address is locked the same way in both places.

        Call on a sudo record: the checks read invoices and orders that the
        portal user cannot read."""
        self.ensure_one()
        locked = {}
        if not self._can_edit_name():
            reason = _(
                "Changing the name is not allowed once invoices have been issued "
                "for this address. Please contact us directly for this operation."
            )
            locked.update(dict.fromkeys(NAME_FIELDS, reason))
        if self._is_other_user_account():
            reason = _(
                "The name and email of a user account cannot be changed here. "
                "Please contact your administrator."
            )
            locked.update(dict.fromkeys((*NAME_FIELDS, "email"), reason))
        elif self._is_portal_email_locked():
            locked["email"] = _(
                "Your email address follows your username. You can change it "
                "in your account security settings."
            )
        return locked

    def _is_other_user_account(self):
        """An internal user's contact, as in the checkout, or the contact of
        another user: its email receives that user's password reset links."""
        # Archived users too: their email gets the reset link once restored
        users = self.with_context(active_test=False).user_ids
        if not users:
            return False
        is_own = self == self.env.user.partner_id
        return not is_own or not all(users.mapped("share"))

    def _is_portal_email_locked(self):
        """The logged-in user's own email is locked when it follows the
        username, as in the checkout. The rule is optional, so it is used
        only when installed."""
        user = self.env.user
        return (
            self == user.partner_id
            and hasattr(user, "_is_partner_email_locked")
            and user._is_partner_email_locked()
        )
