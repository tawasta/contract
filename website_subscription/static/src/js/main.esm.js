/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import {jsonrpc} from "@web/core/network/rpc_service";

publicWidget.registry.PortalSubscription = publicWidget.Widget.extend({
    selector: ".portal_subscription",

    /**
     * @override
     */
    start: function () {
        $("#cancel_subscription_modal").on("show.bs.modal", function (e) {
            var cancelSubscription = $(e.relatedTarget).data("subscription-id");
            $(e.currentTarget)
                .find('input[name="cancel_subscription_id"]')
                .val(cancelSubscription);
        });

        $(document).on("click", "#delete-subscription-confirm", function () {
            var subscriptionValue = document.getElementsByName(
                "cancel_subscription_id"
            )[0].value;
            var action = "/subscription/cancel/" + subscriptionValue;
            $("#cancel_subscription_modal").modal("hide");
            jsonrpc(action, "call", {}).then(function () {
                location.reload();
            });
        });

        $(document).on("click", "#delete-subscription-line-confirm", function () {
            var subscriptionLineValue = $("#cancel_subscription_line_id")[0].value;
            var action = "/subscription/line/cancel/" + subscriptionLineValue;
            $("#cancel_subscription_line_modal").modal("hide");
            jsonrpc(action, "call", {}).then(function () {
                location.reload();
            });
        });

        return this._super.apply(this, arguments);
    },
});

export default publicWidget.registry.PortalSubscription;
