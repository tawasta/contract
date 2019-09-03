# -*- coding: utf-8 -*-
from odoo import fields, models, api


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    show_period_on_lines = fields.Boolean(
        string='Show Invoice Period on Lines',
        help="If this is checked, each generated invoice line will \
        also show the time span of the invoice")

    invoicing_period_date_from = fields.Date(
        string="Next period start",
        compute='_compute_invoice_period',
    )
    invoicing_period_date_to = fields.Date(
        string="Next period end",
        compute='_compute_invoice_period',
    )

    def _compute_invoice_period(self):
        for record in self:
            context = record.get_invoice_context()

            record.invoicing_period_date_from = context['date_from']
            record.invoicing_period_date_to = context['date_to']

    @api.model
    def _prepare_invoice_line(self, line, invoice_id):

        invoice_line_vals =\
            super(AccountAnalyticAccount, self)._prepare_invoice_line(
                line, invoice_id
            )

        if self.show_period_on_lines:
            context = self.get_invoice_context()
            date_format = context.get('date_format', '%m/%d/%Y')

            # Add the invoicing period after line
            invoice_line_vals['name'] += " %s - %s" % (
                context['date_from'].strftime(date_format),
                context['date_to'].strftime(date_format))

        return invoice_line_vals
