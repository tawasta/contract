import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class SaleSubscriptionLine(models.Model):
    _inherit = "sale.subscription.line"

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    @api.model
    def _split_semicolon_parts(self, text):
        """Split by ';', trim, drop empties."""
        if not text:
            _logger.info("cron_split: Split empty text -> []")
            return []
        parts = [p.strip() for p in text.split(";")]
        result = [p for p in parts if p]
        _logger.info("cron_split: Split '%s' -> %s", text, result)
        return result

    @api.model
    def _strip_partner_suffix(self, part, partner_name):
        """
        Remove trailing ', <partner_name>' from part if present.
        """
        part = (part or "").strip()
        partner_name = (partner_name or "").strip()
        if not part or not partner_name:
            return part

        part_low = part.lower()

        suffix = (", " + partner_name).lower()
        if part_low.endswith(suffix):
            stripped = part[: -len(", " + partner_name)].strip()
            _logger.info(
                "cron_split: Strip partner suffix '%s' - '%s' -> '%s'",
                part,
                partner_name,
                stripped,
            )
            return stripped

        suffix2 = ("," + partner_name).lower()
        if part_low.endswith(suffix2):
            stripped = part[: -len("," + partner_name)].strip()
            _logger.info(
                "cron_split: Strip partner suffix '%s' - '%s' -> '%s'",
                part,
                partner_name,
                stripped,
            )
            return stripped

        return part

    @api.model
    def _get_or_create_product_for_part(self, name):
        """
        Return product.product for given name.
        Avoid duplicates by searching product.product by exact template name.

        NOTE:
        - We do NOT use product.template anywhere.
        - Creating product.product will automatically create
          the underlying template/variant as needed by Odoo,
          but we only interact with product.product.
        """
        name = (name or "").strip()
        if not name:
            _logger.info("cron_split: Product name empty -> skip product creation")
            return False

        Product = self.env["product.product"].sudo()

        # Search by exact template name to avoid duplicates
        prod = Product.search([("product_tmpl_id.name", "=", name)], limit=1)
        if prod:
            _logger.info(
                "cron_split: Product exists: '%s' (product_id=%s, template_id=%s)",
                name,
                prod.id,
                prod.product_tmpl_id.id if prod.product_tmpl_id else None,
            )
            return prod

        # Create directly on product.product (no product.template usage)
        prod = Product.create(
            {
                "name": name,
                "type": "service",
                "subscribable": True,
            }
        )
        _logger.info(
            "cron_split: Product created: '%s' (product_id=%s, template_id=%s)",
            name,
            prod.id,
            prod.product_tmpl_id.id if prod.product_tmpl_id else None,
        )
        return prod

    # -------------------------------------------------------------------------
    # SQL helper: backfill stored related company_id for ONE line if NULL
    # -------------------------------------------------------------------------

    @api.model
    def _sql_backfill_line_company_from_subscription(
        self, line_id, subscription_company_id
    ):
        """
        sale.subscription.line.company_id is a stored
        related field and can be NULL in old/imported data.
        OCA compute uses record.company_id and crashes if it's empty.
        We backfill the DB column directly for THIS line.
        """
        if not line_id or not subscription_company_id:
            return 0

        self.env.cr.execute(
            """
            UPDATE sale_subscription_line
               SET company_id = %s
             WHERE id = %s
               AND company_id IS NULL
            """,
            (subscription_company_id, int(line_id)),
        )
        updated = self.env.cr.rowcount or 0
        _logger.info(
            "cron_split: SQL backfill line.company_id from subscription company "
            "line_id=%s company_id=%s updated=%s",
            line_id,
            subscription_company_id,
            updated,
        )
        return updated

    # -------------------------------------------------------------------------
    # Cron
    # -------------------------------------------------------------------------

    @api.model
    def cron_split_lines_by_semicolon(self, limit=500, line_id=None):
        """
        Cron job:
        - If line_id is provided: process ONLY that line (if it contains ';')
        - Otherwise: find subscription lines where name contains ';' (up to limit)

        Process logic:
        - Split name into parts
        - Update original line for first part
        - Create NEW lines for remaining parts (NO copy())
        - Description (line.name) keeps full part text
        - Product name strips ', Partner' if present
        - Attach existing product or create new (no duplicates by name)

        Safety:
        - If line.company_id is NULL (stored related broken),
          backfill it from subscription.company_id via SQL
          BEFORE any write that triggers recompute.
        """
        Line = self.sudo()

        _logger.info("cron_split: START limit=%s line_id=%s", limit, line_id)

        # If a specific line_id is provided -> process only that line
        if line_id:
            line = Line.browse(int(line_id))
            if not line.exists():
                _logger.info(
                    "cron_split: line_id=%s not found -> nothing to do", line_id
                )
                return True

            if not line.name or ";" not in line.name:
                _logger.info(
                    "cron_split: line_id=%s has no ';' in name ('%s') -> skip",
                    line_id,
                    line.name,
                )
                return True

            lines = line
            _logger.info(
                "cron_split: processing single line id=%s name='%s'", line.id, line.name
            )
        else:
            lines = Line.search([("name", "ilike", "%;%")], limit=limit, order="id asc")
            _logger.info("cron_split: found %s lines matching ';'", len(lines))

        processed = 0
        skipped = 0
        created_lines = 0
        updated_lines = 0

        for line in lines:
            processed += 1

            subscription = line.sale_subscription_id
            if not subscription:
                skipped += 1
                _logger.info(
                    "cron_split: SKIP line_id=%s (no sale_subscription_id) name='%s'",
                    line.id,
                    line.name,
                )
                continue

            # Ensure subscription has company (normally required=True, but keep safe)
            if not subscription.company_id:
                # fallback to env.company
                if self.env.company:
                    subscription.write({"company_id": self.env.company.id})
                    _logger.info(
                        "cron_split: set subscription.company_id -> %s (sub_id=%s)",
                        self.env.company.id,
                        subscription.id,
                    )

            # CRITICAL: if line.company_id is NULL in DB (broken stored related),
            # backfill it from subscription.company_id
            # BEFORE any write triggers recompute.
            # Note: line.company_id may still *read* as
            # None due to cache; we re-browse after SQL.
            if subscription.company_id:
                self._sql_backfill_line_company_from_subscription(
                    line.id, subscription.company_id.id
                )
                line = Line.browse(line.id)  # re-read from DB
                subscription = line.sale_subscription_id

            original_name = (line.name or "").strip()
            parts = self._split_semicolon_parts(original_name)
            if len(parts) < 2:
                skipped += 1
                continue

            partner_name = subscription.partner_id.name or ""
            taxes_ids = line.tax_ids.ids

            # 1) Update original line with first part
            first_part = parts[0]
            first_product_name = self._strip_partner_suffix(first_part, partner_name)
            first_product = self._get_or_create_product_for_part(first_product_name)

            vals_first = {
                "product_id": first_product.id if first_product else False,
                "tax_ids": [(6, 0, taxes_ids)],
            }

            line.write(vals_first)
            updated_lines += 1

            # 2) Create NEW lines for remaining parts (NO copy())
            for idx, part in enumerate(parts[1:], start=2):  # Noqa: B007
                product_name = self._strip_partner_suffix(part, partner_name)
                product = self._get_or_create_product_for_part(product_name)

                vals_new = {
                    "sale_subscription_id": subscription.id,
                    "product_id": product.id if product else False,
                    "tax_ids": [(6, 0, taxes_ids)],
                    "product_uom_qty": line.product_uom_qty,
                }

                new_line = Line.create(vals_new)
                created_lines += 1

                # Backfill new line too, just in case (shouldn't be needed, but safe)
                if subscription.company_id:
                    self._sql_backfill_line_company_from_subscription(
                        new_line.id, subscription.company_id.id
                    )
                    new_line = Line.browse(new_line.id)

        return True
