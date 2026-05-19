from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from fastapi.encoders import jsonable_encoder

from odoo.api import Environment

from odoo.addons.fastapi_auth_api_key.dependencies import (
    authenticated_env_by_auth_api_key,
)
from odoo.addons.fastapi_rest_log.services.rest_logger import log_fastapi_call

router = APIRouter(tags=["subscription_api"])

AuthEnv = Annotated[Environment, Depends(authenticated_env_by_auth_api_key)]


def _get_client_ip(request: Request) -> str:
    # Helper module for logging IP the request came from.
    # TODO: this functionality could be in a common helper module
    xff = request.headers.get("x-forwarded-for", "")
    if xff:
        return xff.split(",")[0].strip()
    return request.client.host if request.client else ""


@router.get("/members/{membership_id}/subscription_status")
def subscription_status(
    request: Request,
    membership_id: str,
    env: AuthEnv,
    member_name: Annotated[str | None, Query()] = None,
    member_email: Annotated[str | None, Query()] = None,
) -> dict:
    # Check if
    # - there is a a partner matching the membership ID.
    # - the partner partner has ongoing subscriptions with a proper subscribable product
    partner = (
        env["res.partner"]
        .sudo()
        .search(
            [("ref", "=", membership_id)],
            limit=1,
        )
    )

    has_active_subscription = False
    if partner:
        active_subscription = (
            env["sale.subscription"]
            .sudo()
            .search(
                [
                    ("partner_id", "=", partner.id),
                    ("stage_id.type", "=", "in_progress"),
                    (
                        "sale_subscription_line_ids.product_id.subscription_api_check_count_as_active",
                        "=",
                        True,
                    ),
                ],
                limit=1,
            )
        )
        has_active_subscription = bool(active_subscription)

    result = {
        "membership_id": membership_id,
        "is_member": bool(has_active_subscription),
    }

    log_fastapi_call(
        env,
        method=request.method,
        path=request.url.path,
        # Log member_name and member_email if provided
        payload={**dict(request.query_params), "membership_id": membership_id},
        response=jsonable_encoder(result),
        status_code=200,
        ip_address=_get_client_ip(request),
    )

    return result
