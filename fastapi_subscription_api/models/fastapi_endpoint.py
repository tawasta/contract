from odoo import fields, models

from ..routers import subscription_api

APP_NAME = "subscription_api"


class FastapiEndpoint(models.Model):
    _inherit = "fastapi.endpoint"

    app = fields.Selection(
        selection_add=[(APP_NAME, "Subscription API")],
        ondelete={APP_NAME: "cascade"},
    )

    def _get_fastapi_routers(self):
        if self.app == APP_NAME:
            return [subscription_api.router]
        return super()._get_fastapi_routers()
