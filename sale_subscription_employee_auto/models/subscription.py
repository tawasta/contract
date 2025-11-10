from odoo import api, models


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    def _ensure_employee_for_partner(self):
        Employee = self.env["hr.employee"].sudo()
        for rec in self:
            partner = rec.partner_id
            if not partner:
                continue

            existing = Employee.search(
                [
                    ("work_contact_id", "=", partner.id),
                    ("company_id", "=", rec.company_id.id),
                ],
                limit=1,
            )

            if existing:
                continue

            vals = {
                "name": partner.name or partner.display_name,
                "company_id": rec.company_id.id,
                "work_contact_id": partner.id,
                "private_email": partner.email or False,
                "work_email": partner.email or False,
                "work_phone": partner.phone or False,
                "mobile_phone": partner.mobile or False,
            }
            Employee.create(vals)

    # 1) Tilauksen starttauspolku
    def action_start_subscription(self):
        res = super().action_start_subscription()
        self.sudo()._ensure_employee_for_partner()
        return res

    # 2) Vaiheenvaihdot (kun mennään in_progress-tyyppiseen vaiheeseen)
    def write(self, values):
        res = super().write(values)
        if "stage_id" in values and values["stage_id"]:
            # Kutsutaan vain jos vaihetta muutettiin; suodatetaan in_progress-tilassa olevat
            self.sudo().filtered(
                lambda s: s.stage_id and s.stage_id.type == "in_progress"
            )._ensure_employee_for_partner()
        return res
