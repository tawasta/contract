# -*- coding: utf-8 -*-


from odoo import fields, models


class AccountAnalyticInvoiceLine(models.Model):

    _inherit = 'account.analytic.invoice.line'

    analytic_id_partner_shipping_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        related='analytic_account_id.partner_shipping_id',
        store=True,
    )

    analytic_id_date_end = fields.Date(
        string='End date',
        related='analytic_account_id.date_end',
        store=True,
    )

    analytic_id_shipping_name = fields.Char(
        related='analytic_account_id.partner_shipping_id.name',
    )
    
    analytic_id_shipping_commercial_partner_id = fields.Many2one(
        comodel_name='res.partner',
        related='analytic_account_id.partner_shipping_id.commercial_partner_id',
    )
    
    analytic_id_shipping_street = fields.Char(
        string='Street',
        related='analytic_account_id.partner_shipping_id.street',
    )

    analytic_id_shipping_street2 = fields.Char(
        string='Street 2',
        related='analytic_account_id.partner_shipping_id.street2',
    )

    analytic_id_shipping_zip = fields.Char(
        string='Zip',
        related='analytic_account_id.partner_shipping_id.zip',
    )

    analytic_id_shipping_city = fields.Char(
        string='City',
        related='analytic_account_id.partner_shipping_id.city',
        store=True,
    )

    analytic_id_shipping_country_id = fields.Many2one(
        comodel_name='res.country',
        string='Country',
        related='analytic_account_id.partner_shipping_id.country_id',
        store=True,
    )
