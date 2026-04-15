from odoo import models


class Website(models.Model):
    _inherit = "website"

    def sale_product_domain(self):
        return super().sale_product_domain() + [
            ("subscribable", "=", False),
        ]