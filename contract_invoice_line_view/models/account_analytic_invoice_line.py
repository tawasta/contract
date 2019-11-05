from odoo import fields, models


class AccountAnalyticInvoiceLine(models.Model):

    _inherit = 'account.analytic.invoice.line'

    analytic_id_partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        related='analytic_account_id.partner_id',
        store=True,
    )

    analytic_id_date_end = fields.Date(
        string='End date',
        related='analytic_account_id.date_end',
        store=True,
    )

    analytic_id_code = fields.Char(
        string='Reference',
        related='analytic_account_id.code',
    )

    analytic_id_street = fields.Char(
        string='Street',
        related='analytic_account_id.partner_id_street',
    )

    analytic_id_street2 = fields.Char(
        string='Street 2',
        related='analytic_account_id.partner_id_street2',
    )

    analytic_id_zip = fields.Char(
        string='Zip',
        related='analytic_account_id.partner_id_zip',
    )

    analytic_id_city = fields.Char(
        string='City',
        related='analytic_account_id.partner_id_city',
        store=True,
    )

    analytic_id_country_id = fields.Many2one(
        comodel_name='res.country',
        string='Country',
        related='analytic_account_id.partner_id_country_id',
        store=True,
    )
