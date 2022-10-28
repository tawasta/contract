[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Pipeline Status](https://gitlab.com/tawasta/odoo/contract/badges/14.0-dev/pipeline.svg)](https://gitlab.com/tawasta/odoo/contract/-/pipelines/)

Contracts
=========

This repository provides features extending Contracts.

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[contract_auditlog](contract_auditlog/) | 14.0.1.0.0 |  | Adds audit log rules for contract and contract line
[contract_cancellation_reason](contract_cancellation_reason/) | 14.0.1.0.0 |  | Contract Cancellation Reason
[contract_comment](contract_comment/) | 14.0.1.0.0 |  | Add comment to contracts
[contract_cost_pricelist](contract_cost_pricelist/) | 14.0.1.1.0 |  | Allow using pricelists for computing line cost on contracts
[contract_customer_contact](contract_customer_contact/) | 14.0.1.0.0 |  | Add customer contact to contracts
[contract_default_invoicing_contact](contract_default_invoicing_contact/) | 14.0.1.0.0 |  | Contract Default invoicing contact
[contract_default_name](contract_default_name/) | 14.0.1.0.0 |  | Default name for contracts lastname firstname
[contract_defaults](contract_defaults/) | 14.0.1.0.0 |  | Allows defining global defaults for contracts
[contract_edit_all_lines](contract_edit_all_lines/) | 14.0.1.0.1 |  | Edit all contract lines at once
[contract_edit_last_date_invoiced](contract_edit_last_date_invoiced/) | 14.0.1.0.2 |  | Allows editing last invoiced date (in case of refunds etc.)
[contract_enable_ending_nonpaid](contract_enable_ending_nonpaid/) | 14.0.1.0.0 |  | Dont set the last_date_invoiced field until the bill is paid
[contract_invoice_address](contract_invoice_address/) | 14.0.1.0.2 |  | Add invoice address to contracts
[contract_invoice_address_details](contract_invoice_address_details/) | 14.0.1.0.0 |  | Add invoice address details to contracts
[contract_invoice_address_on_tree_view](contract_invoice_address_on_tree_view/) | 14.0.1.0.0 |  | Adds invoice address to contract tree view
[contract_invoice_line_view](contract_invoice_line_view/) | 14.0.1.0.0 |  | Add a readonly contract invoice line view
[contract_invoice_lines_quantity_invisible](contract_invoice_lines_quantity_invisible/) | 14.0.1.0.0 |  | Use this module to hide contract's quantity-field on invoice lines
[contract_line_change_product_variant](contract_line_change_product_variant/) | 14.0.1.0.2 |  | Contract Line Change product variant
[contract_line_cost](contract_line_cost/) | 14.0.1.1.0 |  | Add cost price to contract lines and move it to the invoice
[contract_line_inline_edit](contract_line_inline_edit/) | 14.0.1.0.1 |  | Allows editing non-fixed contract lines inline
[contract_line_list_view](contract_line_list_view/) | 14.0.1.0.0 |  | Adds list view of contract lines
[contract_line_optional_fields](contract_line_optional_fields/) | 14.0.1.0.1 |  | Set contract line fields as optional, so users can hide them
[contract_line_partner_address_label](contract_line_partner_address_label/) | 14.0.1.0.0 |  | Contract Line Partner Address Label
[contract_line_stop_ignore_last_date_invoice](contract_line_stop_ignore_last_date_invoice/) | 14.0.1.0.0 |  | When stopping a contract line, the 'Last Date Invoiced' is ignored
[contract_line_variant_company](contract_line_variant_company/) | 14.0.1.0.0 |  | Contract Line Variant Company
[contract_link_another_contract](contract_link_another_contract/) | 14.0.1.0.0 |  | Contract link to another contract
[contract_mass_action_invoice_member](contract_mass_action_invoice_member/) | 14.0.1.0.1 |  | Mass action to set default invoice address and create a new invoice
[contract_membership_integration](contract_membership_integration/) | 14.0.1.3.2 |  | Show memberships in contract, and end the membership if contract line is ended
[contract_name_from_customer_name_and_product_name](contract_name_from_customer_name_and_product_name/) | 14.0.1.0.0 |  | Customer & Product Name is used as Contract's name
[contract_note_to_invoice_comment](contract_note_to_invoice_comment/) | 14.0.1.0.0 |  | Contract note content is updated to invoice's comment field
[contract_partner_ref](contract_partner_ref/) | 14.0.1.0.0 |  | Contract Partner Ref
[contract_partners_invoice_method](contract_partners_invoice_method/) | 14.0.1.0.0 |  | Contract Customer Invoice Transmission Method
[contract_portal_date_end](contract_portal_date_end/) | 14.0.1.0.0 |  | Show Date End on Contract Portal Views
[contract_portal_date_start](contract_portal_date_start/) | 14.0.1.0.0 |  | Show Date Start on Contract Portal Views
[contract_portal_invoice_address](contract_portal_invoice_address/) | 14.0.1.0.0 |  | Contract portal invoice address
[contract_portal_product_default_code](contract_portal_product_default_code/) | 14.0.1.0.0 |  | Show Product Default Code on Contract Portal Views
[contract_product_analytic_tags](contract_product_analytic_tags/) | 14.0.1.0.0 |  | Adds contract line analytic tags from products
[contract_recurring_invoice_queue](contract_recurring_invoice_queue/) | 14.0.1.0.2 |  | Create recurring invoices as queued jobs
[contract_remove_unlink_right](contract_remove_unlink_right/) | 14.0.1.0.0 |  | Contract remove unlink right
[contract_send_messages](contract_send_messages/) | 14.0.1.0.0 |  | Contract line messages
[contract_shipping_address](contract_shipping_address/) | 14.0.1.0.1 |  | Add shipping address to contracts
[contract_stop_ignore_recurring_next_date](contract_stop_ignore_recurring_next_date/) | 14.0.1.0.0 |  | When contract is stopped, clear the recurring next date
[contract_template](contract_template/) | 14.0.1.0.0 |  | Contract Template
[contract_use_existing_invoice](contract_use_existing_invoice/) | 14.0.1.0.0 |  | Add lines to an existing invoice instead of creating a new invoice
[generate_recurring_invoices_from_contracts_limit](generate_recurring_invoices_from_contracts_limit/) | 14.0.1.0.0 |  | Define limit to how many invoices to generate at a time. Defaults to 5000.
[website_stop_contract_line](website_stop_contract_line/) | 14.0.1.0.0 |  | Website stop contract line
[website_upgrade_contract_line](website_upgrade_contract_line/) | 14.0.1.0.0 |  | Website upgrade contract line

[//]: # (end addons)
