from odoo import models


class Product(models.Model):
    _inherit = "product.product"

    def get_product_multiline_description_sale(self):
        res = super().get_product_multiline_description_sale()

        if (
            self.subscription_template_id
            and self.subscription_template_id.auto_period_markers
        ):
            res += " {}".format(self.subscription_template_id.auto_period_markers_text)

        return res
