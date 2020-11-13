# -*- coding: utf-8 -*-
from odoo import api
from odoo import fields
from odoo import models


class AccountAnalyticInvoiceLine(models.Model):

    _inherit = 'account.analytic.invoice.line'

    analytic_id_partner_invoice_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        related='analytic_account_id.partner_invoice_id',
        store=True,
    )

    analytic_id_invoice_name = fields.Char(
        related='analytic_account_id.partner_invoice_id.name',
    )

    analytic_id_invoice_name_conditional = fields.Char(
        string="Name",
        compute='_compute_analytic_id_invoice_name_conditional'
    )
    
    analytic_id_invoice_commercial_partner_id = fields.Many2one(
        comodel_name='res.partner',
        related='analytic_account_id.partner_invoice_id.commercial_partner_id',
    )
    
    analytic_id_invoice_street = fields.Char(
        string='Street',
        related='analytic_account_id.partner_invoice_id.street',
    )

    analytic_id_invoice_street2 = fields.Char(
        string='Street 2',
        related='analytic_account_id.partner_invoice_id.street2',
    )

    analytic_id_invoice_zip = fields.Char(
        string='Zip',
        related='analytic_account_id.partner_invoice_id.zip',
    )

    analytic_id_invoice_city = fields.Char(
        string='City',
        related='analytic_account_id.partner_invoice_id.city',
        store=True,
    )

    analytic_id_invoice_country_id = fields.Many2one(
        comodel_name='res.country',
        string='Country',
        related='analytic_account_id.partner_invoice_id.country_id',
        store=True,
    )

    analytic_id_invoice_user_id = fields.Many2one(
        comodel_name='res.users',
        string='Salesperson',
        related='analytic_account_id.partner_invoice_id.user_id',
        store=True,
    )

    @api.multi
    def _compute_analytic_id_invoice_name_conditional(self):
        for record in self:
            if record.analytic_id_partner_invoice_id != \
                    record.analytic_id_invoice_commercial_partner_id:
                record.analytic_id_invoice_name_conditional = \
                    record.analytic_account_id.partner_invoice_id.name
