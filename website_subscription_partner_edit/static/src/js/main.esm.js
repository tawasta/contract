/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import {jsonrpc} from "@web/core/network/rpc_service";
import Dialog from "@web/legacy/js/core/dialog";
import {_t} from "@web/core/l10n/translation";

const SELECTED_CARD_CLASS = "o_wspe_selected";

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
            "input[name='is_company']",
            this._onToggleIsCompany.bind(this)
        );

        // The modal is added to the body, outside of this widget
        $(document).on(
            "keydown",
            ".contact-card",
            this._onContactCardKeydown.bind(this)
        );

        $(document).on(
            "change",
            "#customer-invoice-transmit-method",
            this._onTransmitMethodChange.bind(this)
        );

        $(document).on(
            "click",
            ".o_edit_invoice_address",
            this._onEditInvoiceAddress.bind(this)
        );
    },

    _onEditInvoiceAddress: function (ev) {
        ev.preventDefault();
        ev.stopPropagation();
        const contactID = $(ev.currentTarget).data("contact-id");
        const subscriptionID = $("#edit_customer_form").data("subscription-id");

        jsonrpc(
            `/my/subscriptions/${subscriptionID}/invoice_address/${contactID}/form`,
            {}
        )
            .then((formContent) => {
                this._clearContactSelection();
                const $addressForm = $("#new_contact_form").html(formContent);
                const scrollToForm = () =>
                    $addressForm[0].scrollIntoView({block: "start"});
                if ($addressForm.hasClass("show")) {
                    scrollToForm();
                } else {
                    $addressForm
                        .one("shown.bs.collapse", scrollToForm)
                        .collapse("show");
                }
            })
            .catch(() => {
                this._showErrorMessage(
                    _t(
                        "The address could not be opened. Reload the page and try again."
                    )
                );
            });
    },

    // The edit form replaces the new address form; bring the new one back
    // so that a selection or a new address is not saved as an edit.
    _restoreNewAddressForm: function () {
        const $addressForm = $("#new_contact_form");
        if ($addressForm.find("input[name='edit_contact_id']").length) {
            $addressForm.html(this.newAddressFormHtml);
        }
    },

    _onTransmitMethodChange: function (ev) {
        const selectedOption = $(ev.currentTarget).find("option:selected");
        const selectedCode = selectedOption.data("code"); // From data-code="method.code"

        const $edicode = $("#edicode-div");
        const $einvoiceOperator = $("#einvoice-operator-div");

        if (selectedCode === "einvoice") {
            $edicode.removeClass("d-none");
            $einvoiceOperator.removeClass("d-none");
        } else {
            $edicode.addClass("d-none");
            $einvoiceOperator.addClass("d-none");
        }
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
                this.newAddressFormHtml = $modal.find("#new_contact_form").html();

                // eslint-disable-next-line no-undef
                const modalBS = new Modal($modal[0], {
                    backdrop: "static",
                    keyboard: false,
                });
                modalBS.show();

                // The address in use starts selected: the new address form is
                // then not required, as when a card is selected by hand
                if ($modal.find(`.contact-card.${SELECTED_CARD_CLASS}`).length) {
                    this._toggleRequiredFields(false);
                }

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

    _onToggleIsCompany: function () {
        // Person and Company are radios of one group: the Company one decides
        const isChecked = $("#is_company_toggle").is(":checked");

        const $alvField = $("#company_registry_group");
        const $alvFieldInput = $("input[name='company_registry']");
        const $companyName = $("#company_name_field");
        const $personNames = $("#person_name_fields");
        // Const $transmitMethod = $("#customer_invoice_transmit_method_id_div");

        if (isChecked) {
            $alvField.removeClass("d-none");
            $alvFieldInput.attr("required", "required");

            $companyName.removeClass("d-none");
            $companyName.find("input").attr("required", "required");

            $personNames.addClass("d-none");
            $personNames.find("input").removeAttr("required");

            // $transmitMethod.removeClass("d-none");
        } else {
            $alvField.addClass("d-none");
            $alvFieldInput.removeAttr("required");

            $companyName.addClass("d-none");
            $companyName.find("input").removeAttr("required");

            $personNames.removeClass("d-none");
            $personNames.find("input").attr("required", "required");

            // $transmitMethod.addClass("d-none");
        }

        $("#customer-invoice-transmit-method option").each(function () {
            const $option = $(this);
            const targetType = $option.data("type");

            // Näytetään vain sopivat tyypit (tai "both")
            if (
                targetType === "both" ||
                (isChecked && targetType === "company") ||
                (!isChecked && targetType === "person")
            ) {
                $option.show();
            } else {
                $option.hide();
            }
        });

        $("#customer-invoice-transmit-method").val("");
    },

    _onSelectContact: function (ev) {
        if ($(ev.target).closest(".o_edit_invoice_address").length) {
            // The edit button of the card opens the address, not selects it
            return;
        }
        ev.preventDefault();
        ev.stopPropagation();
        this._selectContactCard($(ev.currentTarget));
    },

    _selectContactCard: function ($card) {
        this._restoreNewAddressForm();
        this._clearContactSelection();
        $card
            .addClass(SELECTED_CARD_CLASS)
            .find(".o_wspe_contact_card_check")
            .attr("aria-checked", "true");
        $("#selected_contact").val($card.attr("data-contact-id"));

        // Piilotetaan uuden kontaktin lomake, jos valitaan olemassa oleva kontakti
        $("#new_contact_form").collapse("hide");

        // Poistetaan required-attribuutit
        this._toggleRequiredFields(false);
    },

    _onToggleNewContact: function (ev) {
        ev.preventDefault();
        ev.stopPropagation();

        // ** Poistetaan kaikki aiemmat valinnat **
        this._clearContactSelection();
        this._restoreNewAddressForm();

        // ** Varmistetaan, että lomake aukeaa aina kun "Add New" painetaan **
        $("#new_contact_form").collapse("show");

        // Lisätään takaisin required-attribuutit
        this._toggleRequiredFields(true);

        this._onToggleIsCompany();
    },

    // The radios of the cards work as a radio group: Enter or Space selects
    // the focused card, the arrow keys move the selection to the next or the
    // previous card
    _onContactCardKeydown: function (ev) {
        if (!$(ev.target).is(".o_wspe_contact_card_check")) {
            return;
        }
        const step = {ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1}[ev.key];
        if (!step && ![" ", "Enter"].includes(ev.key)) {
            return;
        }
        ev.preventDefault();
        let $card = $(ev.currentTarget);
        if (step) {
            const $cards = $card.closest("[role='radiogroup']").find(".contact-card");
            $card = $cards.eq(
                ($cards.index($card) + step + $cards.length) % $cards.length
            );
            $card.find(".o_wspe_contact_card_check").trigger("focus");
        }
        this._selectContactCard($card);
    },

    _clearContactSelection: function () {
        $(".contact-card")
            .removeClass(SELECTED_CARD_CLASS)
            .find(".o_wspe_contact_card_check")
            .attr("aria-checked", "false");
        $("#selected_contact").val("");
    },

    _onFormSubmit: function (ev) {
        ev.preventDefault();
        ev.stopPropagation();

        const $form = $(ev.currentTarget);
        const actionUrl = $form.attr("action");
        const formData = new FormData($form[0]);
        this._setSaving($form, true);

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
            error: () => {
                this._showErrorMessage(
                    _t(
                        "The changes could not be saved. Check your connection and try again."
                    )
                );
            },
            complete: () => {
                this._setSaving($form, false);
            },
        });
    },

    _toggleRequiredFields: function (isRequired) {
        const fields = ["name", "zip", "city", "street", "firstname", "lastname"];

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
            $content: $("<div/>").text(message),
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

    // The save button shows the progress and cannot be clicked twice
    _setSaving: function ($form, isSaving) {
        const $button = $form.find("button[type='submit']");
        $button.prop("disabled", isSaving).attr("aria-busy", isSaving);
        $button.find(".o_saving_spinner").remove();
        if (isSaving) {
            $button.prepend(
                $("<span/>", {
                    class: "o_saving_spinner spinner-border spinner-border-sm me-2",
                    "aria-hidden": "true",
                })
            );
        }
    },

    _showErrorMessage: function (message) {
        new Dialog(this, {
            title: _t("The changes were not saved"),
            size: "medium",
            // Several errors come on lines of their own
            $content: $("<div/>", {class: "text-prewrap text-break"}).text(message),
            buttons: [{text: _t("Close"), close: true}],
        }).open();
    },
});

publicWidget.registry.PartnerUpgrade = PartnerUpgrade;
