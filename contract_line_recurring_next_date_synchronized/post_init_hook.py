def init_contract_invoice_dates(env):
    env["contract.contract"].search([])._compute_recurring_next_date_synchronized()
