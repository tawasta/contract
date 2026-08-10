import logging

_logger = logging.getLogger(__name__)


def post_init_hook(env):
    """Populate the flag for existing partners on install."""
    _logger.info("Computing has_overdue_subscription_invoices for existing partners")
    env["res.partner"]._cron_update_overdue_subscription_invoices()
