[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Pre-commit Status](https://github.com/tawasta/contract/actions/workflows/pre-commit.yml/badge.svg?branch=17.0)](https://github.com/tawasta/contract/actions/workflows/pre-commit.yml?query=branch%3A17.0)

Contracts
=========

This repository provides features extending Contracts.

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[contract_auditlog](contract_auditlog/) | 17.0.1.0.0 |  | Adds audit log rules for contract and contract line
[contract_default_name](contract_default_name/) | 17.0.1.0.0 |  | Default name for contracts lastname firstname
[contract_edit_all_lines_next_invoice_date](contract_edit_all_lines_next_invoice_date/) | 17.0.1.0.0 |  | Edit all contract's lines' Date of Next Invoice at once
[contract_edit_last_date_invoiced](contract_edit_last_date_invoiced/) | 17.0.1.0.0 |  | Allows editing last invoiced date (in case of refunds etc.)
[contract_invoice_address](contract_invoice_address/) | 17.0.1.0.0 |  | Add invoice address to contracts and force its commercial partner
[contract_line_helper_fields](contract_line_helper_fields/) | 17.0.1.0.1 |  | Helper fields for contract lines to help searching related information
[contract_line_list_view](contract_line_list_view/) | 17.0.1.0.0 |  | Adds list view of contract lines
[contract_line_optional_fields](contract_line_optional_fields/) | 17.0.1.0.0 |  | Set contract line fields as optional, so users can hide them
[contract_line_partner](contract_line_partner/) | 17.0.1.0.0 |  | Allows defining a partner to contract lines
[contract_line_recurring_defaults](contract_line_recurring_defaults/) | 17.0.1.0.0 |  | Allows defining global defaults for contract lines
[contract_line_recurring_next_date_synchronized](contract_line_recurring_next_date_synchronized/) | 17.0.1.0.0 |  | Add information about next contract invoicing if they are synchronized
[contract_line_stop_ignore_last_date_invoice](contract_line_stop_ignore_last_date_invoice/) | 17.0.1.0.0 |  | When stopping a contract line, the 'Last Date Invoiced' is ignored
[contract_link_another_contract](contract_link_another_contract/) | 17.0.1.0.0 |  | Shows all contracts with the same payee on the main contract
[contract_mass_create_invoices](contract_mass_create_invoices/) | 17.0.1.0.0 |  | Manually create invoices for multiple contracts
[contract_mass_edit_lines](contract_mass_edit_lines/) | 17.0.1.0.0 |  | Allows mass editing contract lines from contract tree view
[contract_optional_fields](contract_optional_fields/) | 17.0.1.0.0 |  | Set contract fields as optional in tree view
[contract_page_partner](contract_page_partner/) | 17.0.1.0.0 |  | Contract Page Partner
[contract_partner_ref](contract_partner_ref/) | 17.0.1.0.0 |  | Show partner membership number in contract views
[contract_portal_date_end](contract_portal_date_end/) | 17.0.1.0.0 |  | Toggleable showing of Date End in Contract Portal View's lines
[contract_portal_date_start](contract_portal_date_start/) | 17.0.1.0.0 |  | Toggleable showing of Date Start on Contract Portal Views
[contract_portal_hide_message_thread](contract_portal_hide_message_thread/) | 17.0.1.0.0 |  | Adds a toggle for hiding the contract messaging section
[contract_portal_invoice_address](contract_portal_invoice_address/) | 17.0.1.0.0 |  | Toggleable showing of contract's invoice address in portal
[contract_portal_product_default_code](contract_portal_product_default_code/) | 17.0.1.0.0 |  | Toggleable showing of internal reference in separate column on contract lines
[contract_product_usage](contract_product_usage/) | 17.0.1.0.0 |  | Show contracts and contract lines where product is used in
[contract_remove_unlink_right](contract_remove_unlink_right/) | 17.0.1.0.0 |  | Disallow deleting contracts (always archive them)
[contract_shipping_address](contract_shipping_address/) | 17.0.1.0.1 |  | Add shipping address to contracts
[contract_template_additional_fields](contract_template_additional_fields/) | 17.0.1.0.0 |  | Adds invoice interval, payment term and responsible person fields to Contract Template
[contract_to_subscription](contract_to_subscription/) | 17.0.1.0.0 |  | Migrate contracts to subscriptions
[contract_use_customer_as_invoicing_contact](contract_use_customer_as_invoicing_contact/) | 17.0.1.0.0 |  | Default value to a contract's invoicing contact
[contract_use_existing_invoice](contract_use_existing_invoice/) | 17.0.1.0.0 |  | Add lines to an existing invoice instead of creating a new invoice
[only_one_subscription_in_cart](only_one_subscription_in_cart/) | 17.0.1.1.0 |  | Allow to have only one subscription in cart
[subscription_auditlog](subscription_auditlog/) | 17.0.1.0.0 |  | Adds audit log rules for sale subscription and subscription line
[subscription_closing](subscription_closing/) | 17.0.1.0.3 |  | Allows ending subscription to a future date
[subscription_customer_reference](subscription_customer_reference/) | 17.0.1.0.0 |  | Add customer reference to subscriptions
[subscription_disable_qty_in_cart](subscription_disable_qty_in_cart/) | 17.0.1.0.0 |  | Disable changing subscription product quantity in cart
[subscription_free_product](subscription_free_product/) | 17.0.1.0.0 |  | Add a free subscription when purchasing a subscription product
[subscription_invoice_queue](subscription_invoice_queue/) | 17.0.1.0.0 |  | Create invoices as queued jobs
[subscription_line_change_product_variant](subscription_line_change_product_variant/) | 17.0.1.1.0 |  | Substriction Line Change product variant and create invoice
[subscription_line_closing](subscription_line_closing/) | 17.0.1.2.0 |  | Allows ending subscription lines without deleting them
[subscription_line_cost](subscription_line_cost/) | 17.0.1.0.0 |  | Allows defining a cost to subscription lines
[subscription_line_list_view](subscription_line_list_view/) | 17.0.1.0.1 |  | Creates a tree view for subscription lines
[subscription_line_partner](subscription_line_partner/) | 17.0.1.0.4 |  | Allows defining a partner to subscription lines
[subscription_line_related_sale_order_line](subscription_line_related_sale_order_line/) | 17.0.1.0.0 |  | Add SO line information for subscription lines
[subscription_modification](subscription_modification/) | 17.0.1.0.1 |  | Add modification log to subscriptions
[subscription_shipping_address](subscription_shipping_address/) | 17.0.1.0.0 |  | Add shipping address to subscriptions
[subscription_usability_improvements](subscription_usability_improvements/) | 17.0.1.0.0 |  | Add basic searches, groupings and optional fields to subscriptions
[subscription_use_existing_invoice](subscription_use_existing_invoice/) | 17.0.1.0.0 |  | Add subscription lines to an existing draft invoice
[subscription_use_existing_subscription](subscription_use_existing_subscription/) | 17.0.1.0.0 |  | Add new subscription lines to existing subscription
[subscription_user_default](subscription_user_default/) | 17.0.1.0.0 |  | Configurable Default or Core User for Sale Subscriptions
[website_subscription](website_subscription/) | 17.0.1.2.2 |  | Subscriptions in website portal
[website_subscription_edit](website_subscription_edit/) | 17.0.1.0.0 |  | Allows editings subscriptions from user portal

[//]: # (end addons)
