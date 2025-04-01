/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import {jsonrpc} from "@web/core/network/rpc_service";
import Dialog from "@web/legacy/js/core/dialog";
import {_t} from "@web/core/l10n/translation";

var PartnerUpgrade = publicWidget.Widget.extend({
    selector: "#customer_information",
    events: {
        "click #modal_customer_edit": "_onClickUpgradeButton",
        "click .contact-card": "_onSelectContact",
    },

    start: function () {
        this._super.apply(this, arguments);
        $(document).on("submit", "#edit_customer_form", this._onFormSubmit.bind(this));

        // Lisätään event listener dynaamisesti lisättyihin elementteihin
        $(document).on(
            "click",
            ".o_wsale_add_address",
            this._onToggleNewContact.bind(this)
        );

        $(document).on(
            "change",
            "#is_company_toggle",
            this._onToggleIsCompany.bind(this)
        );
    },

    _onClickUpgradeButton: function (ev) {
        ev.preventDefault();
        ev.stopPropagation();
        const partnerID = $(ev.currentTarget).attr("partner-id");
        const subscriptionID = $(ev.currentTarget).attr("subscription-id");

        if (!partnerID || !subscriptionID) {
            console.error("PARTNER ID or SUBSCRIPTION ID not found.");
            return;
        }

        jsonrpc(
            `/partner/${partnerID}/subscription/${subscriptionID}/upgrade/modal`,
            {}
        )
            .then((modalContent) => {
                const $modal = $(modalContent);
                $modal.find(".modal-body > div").removeClass("container");
                $modal.appendTo(document.body);

                // eslint-disable-next-line no-undef
                const modalBS = new Modal($modal[0], {
                    backdrop: "static",
                    keyboard: false,
                });
                modalBS.show();

                $modal.on("click", ".btn-close", function () {
                    $modal.remove();
                });
                $modal.on("hidden.bs.modal", function () {
                    $modal.remove();
                });

                // Re-initialize click event on contact cards
                $(".contact-card")
                    .off("click")
                    .on("click", this._onSelectContact.bind(this));
            })
            .catch((err) => {
                console.error("Failed to load modal content", err);
            });
    },

    _onToggleIsCompany: function (ev) {
        const isChecked = $(ev.currentTarget).is(":checked");
        console.log(isChecked);
        const $alvField = $("#company_registry_group");
        console.log($alvField);
        if (isChecked) {
            $alvField.removeClass("d-none");
        } else {
            $alvField.addClass("d-none");
        }
    },

    _onSelectContact: function (ev) {
        ev.preventDefault();
        ev.stopPropagation();

        const $selectedCard = $(ev.currentTarget);

        // Poistetaan valinta kaikilta korteilta
        $(".contact-card").removeClass("bg-primary border border-primary text-white");

        // Lisätään valinta valitulle kortille
        $selectedCard.addClass("bg-primary border border-primary text-white");

        const contactId = $selectedCard.attr("data-contact-id");
        $("#selected_contact").val(contactId);

        // Piilotetaan uuden kontaktin lomake, jos valitaan olemassa oleva kontakti
        $("#new_contact_form").collapse("hide");

        // Poistetaan required-attribuutit
        this._toggleRequiredFields(false);
    },

    _onToggleNewContact: function (ev) {
        ev.preventDefault();
        ev.stopPropagation();

        // ** Poistetaan kaikki aiemmat valinnat **
        $(".contact-card").removeClass("bg-primary border border-primary text-white");
        $("#selected_contact").val("");

        // ** Varmistetaan, että lomake aukeaa aina kun "Add New" painetaan **
        $("#new_contact_form").collapse("show");

        // Lisätään takaisin required-attribuutit
        this._toggleRequiredFields(true);
    },

    _onFormSubmit: function (ev) {
        ev.preventDefault();
        ev.stopPropagation();

        const $form = $(ev.currentTarget);
        const actionUrl = $form.attr("action");
        const formData = new FormData($form[0]);
        this._showLoadingScreen();

        $.ajax({
            url: actionUrl,
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: (response) => {
                const jsonResponse = JSON.parse(response);

                if (jsonResponse.error) {
                    this._showErrorMessage(jsonResponse.msg);
                } else {
                    this._showSuccessMessage(jsonResponse.msg);
                    $form.closest(".modal").modal("hide");
                }
            },
            error: (err) => {
                console.error("Form submission failed:", err);
                this._showErrorMessage("An unexpected error occurred.");
            },
            complete: () => {
                this._hideLoadingScreen();
            },
        });
    },

    _toggleRequiredFields: function (isRequired) {
        const fields = ["name", "zip", "city", "street"];

        fields.forEach((field) => {
            const input = $(`input[name='${field}']`);
            if (isRequired) {
                input.attr("required", "required");
            } else {
                input.removeAttr("required");
            }
        });
    },

    _showSuccessMessage: function (message) {
        new Dialog(this, {
            title: _t("Success"),
            size: "medium",
            $content: $("<div/>").html(message),
            buttons: [
                {
                    text: _t("OK"),
                    close: true,
                    click: function () {
                        location.reload();
                    },
                },
            ],
        }).open();
    },

    _showLoadingScreen: function () {
        const loadingMessage = `
            <div id="loading-screen" style="
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, 0.5);
                z-index: 9999;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #fff;
                font-size: 20px;">
                <div>
                    <div class="spinner-border text-light" role="status"></div>
                    <p>Loading, please wait...</p>
                </div>
            </div>`;
        $("body").append(loadingMessage);
    },

    _hideLoadingScreen: function () {
        $("#loading-screen").remove();
    },

    _showErrorMessage: function (message) {
        alert(`Error: ${message}`);
    },
});

publicWidget.registry.PartnerUpgrade = PartnerUpgrade;
