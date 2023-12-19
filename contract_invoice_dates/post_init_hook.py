from odoo import SUPERUSER_ID, api


def init_contract_invoice_dates(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env["contract.contract"].search([])._compute_recurring_next_date_synchronized()
