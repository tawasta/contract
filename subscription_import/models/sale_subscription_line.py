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
        """Remove trailing ', <partner_name>' from part if present."""
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
        """Return product.product for given name. Avoid duplicates by template exact name."""
        name = (name or "").strip()
        if not name:
            _logger.info("cron_split: Product name empty -> skip product creation")
            return False

        Template = self.env["product.template"].sudo()

        tmpl = Template.search([("name", "=", name)], limit=1)
        if tmpl:
            _logger.info(
                "cron_split: Product exists: '%s' (template_id=%s, variant_id=%s)",
                name,
                tmpl.id,
                tmpl.product_variant_id.id,
            )
            return tmpl.product_variant_id

        tmpl = Template.create(
            {
                "name": name,
                "type": "service",
                "subscribable": True,
            }
        )
        _logger.info(
            "cron_split: Product created: '%s' (template_id=%s, variant_id=%s)",
            name,
            tmpl.id,
            tmpl.product_variant_id.id,
        )
        return tmpl.product_variant_id

    # -------------------------------------------------------------------------
    # Critical fix: backfill stored related company_id on subscription lines
    # -------------------------------------------------------------------------

    @api.model
    def _sql_backfill_line_company(self, subscription_id, company_id, line_ids=None):
        """
        sale.subscription.line.company_id is a stored related field and may be NULL in old data.
        OCA compute uses record.company_id and crashes if it's empty.
        This backfills DB column sale_subscription_line.company_id from subscription.company_id.

        If line_ids provided -> only those ids, otherwise all lines of the subscription.
        """
        if not subscription_id or not company_id:
            return 0

        if line_ids:
            ids = [int(x) for x in line_ids if x]
            if not ids:
                return 0
            # update only NULL company_id rows
            query = """
                UPDATE sale_subscription_line
                   SET company_id = %s
                 WHERE id = ANY(%s)
                   AND company_id IS NULL
            """
            self.env.cr.execute(query, (company_id, ids))
        else:
            query = """
                UPDATE sale_subscription_line
                   SET company_id = %s
                 WHERE sale_subscription_id = %s
                   AND company_id IS NULL
            """
            self.env.cr.execute(query, (company_id, subscription_id))

        count = self.env.cr.rowcount or 0
        _logger.info(
            "cron_split: SQL backfill company_id=%s on sale_subscription_line (sub_id=%s, line_ids=%s) -> updated=%s",
            company_id,
            subscription_id,
            line_ids if line_ids else "ALL_SUB_LINES",
            count,
        )
        return count

    # -------------------------------------------------------------------------
    # Cron
    # -------------------------------------------------------------------------

    @api.model
    def cron_split_lines_by_semicolon(self, limit=500, line_id=None):
        """
        Split subscription line.name by ';' into multiple lines.
        Uses CREATE (no copy). Also fixes NULL stored related company_id on lines via SQL.
        """
        Line = self.sudo()

        _logger.info("cron_split: START limit=%s line_id=%s", limit, line_id)

        if line_id:
            line = Line.browse(int(line_id))
            if not line.exists():
                _logger.info("cron_split: line_id=%s not found -> nothing to do", line_id)
                return True
            if not line.name or ";" not in line.name:
                _logger.info("cron_split: line_id=%s has no ';' in name ('%s') -> skip", line_id, line.name)
                return True
            lines = line
            _logger.info("cron_split: processing single line id=%s name='%s'", line.id, line.name)
        else:
            lines = Line.search([("name", "ilike", "%;%")], limit=limit, order="id asc")
            _logger.info("cron_split: found %s lines matching ';'", len(lines))

        processed = skipped = created_lines = updated_lines = 0

        for line in lines:
            processed += 1

            subscription = line.sale_subscription_id
            if not subscription:
                skipped += 1
                _logger.info("cron_split: SKIP line_id=%s (no sale_subscription_id) name='%s'", line.id, line.name)
                continue

            # Determine target company robustly
            target_company = subscription.company_id or self.env.company
            if not target_company:
                target_company = self.env["res.company"].sudo().search([], limit=1)

            _logger.info(
                "cron_split: LINE line_id=%s sub_id=%s partner='%s' line_company_id=%s sub_company_id=%s target_company_id=%s name='%s'",
                line.id,
                subscription.id,
                subscription.partner_id.name or "",
                line.company_id.id if line.company_id else None,
                subscription.company_id.id if subscription.company_id else None,
                target_company.id if target_company else None,
                line.name or "",
            )

            if not target_company:
                skipped += 1
                _logger.info("cron_split: SKIP line_id=%s (no target company found)", line.id)
                continue

            # 1) Ensure subscription has company (should already, but keep safe)
            if not subscription.company_id:
                subscription.write({"company_id": target_company.id})
                _logger.info(
                    "cron_split: set subscription.company_id -> %s (sub_id=%s)",
                    target_company.id,
                    subscription.id,
                )

            # 2) CRITICAL: Backfill NULL line.company_id (stored related) in DB BEFORE any recompute triggers
            #    - do for all lines of the subscription (covers original + any other broken rows)
            self._sql_backfill_line_company(subscription.id, subscription.company_id.id, line_ids=None)

            # invalidate cache so ORM sees updated company_id
            subscription.sale_subscription_line_ids.invalidate_cache(fnames=["company_id"])
            line.invalidate_cache(fnames=["company_id"])

            original_name = (line.name or "").strip()
            parts = self._split_semicolon_parts(original_name)
            if len(parts) < 2:
                skipped += 1
                _logger.info("cron_split: SKIP line_id=%s parts=%s (<2) original='%s'", line.id, parts, original_name)
                continue

            partner_name = subscription.partner_id.name or ""
            taxes_ids = line.tax_ids.ids

            _logger.info(
                "cron_split: splitting line_id=%s into %s parts, taxes=%s partner='%s'",
                line.id,
                len(parts),
                taxes_ids,
                partner_name,
            )

            # Update original line with first part
            first_part = parts[0]
            first_desc = first_part
            first_product_name = self._strip_partner_suffix(first_part, partner_name)
            first_product = self._get_or_create_product_for_part(first_product_name)

            vals_first = {
                "name": first_desc,
                "product_id": first_product.id if first_product else False,
                "tax_ids": [(6, 0, taxes_ids)],
            }

            _logger.info(
                "cron_split: update ORIGINAL line_id=%s desc='%s' product_name='%s' product_id=%s taxes=%s line_company_id_now=%s",
                line.id,
                first_desc,
                first_product_name,
                first_product.id if first_product else None,
                taxes_ids,
                line.company_id.id if line.company_id else None,
            )
            line.write(vals_first)
            updated_lines += 1

            # Create NEW lines for remaining parts
            for idx, part in enumerate(parts[1:], start=2):
                desc = part
                product_name = self._strip_partner_suffix(part, partner_name)
                product = self._get_or_create_product_for_part(product_name)

                vals_new = {
                    "sale_subscription_id": subscription.id,
                    "name": desc,
                    "product_id": product.id if product else False,
                    "tax_ids": [(6, 0, taxes_ids)],
                    "product_uom_qty": line.product_uom_qty,
                }

                new_line = Line.create(vals_new)
                created_lines += 1

                # Backfill company_id for the new line too (belt-and-suspenders)
                self._sql_backfill_line_company(subscription.id, subscription.company_id.id, line_ids=[new_line.id])
                new_line.invalidate_cache(fnames=["company_id"])

                _logger.info(
                    "cron_split: created NEW line %s/%s new_line_id=%s sub_id=%s desc='%s' product_name='%s' product_id=%s taxes=%s new_line_company_id=%s",
                    idx,
                    len(parts),
                    new_line.id,
                    subscription.id,
                    desc,
                    product_name,
                    product.id if product else None,
                    taxes_ids,
                    new_line.company_id.id if new_line.company_id else None,
                )

        _logger.info(
            "cron_split: END processed=%s skipped=%s created_lines=%s updated_lines=%s",
            processed,
            skipped,
            created_lines,
            updated_lines,
        )
        return True
