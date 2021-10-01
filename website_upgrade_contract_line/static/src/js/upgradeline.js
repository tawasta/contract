odoo.define('website_upgrade_contract_line.portal_contract_page', function (require) {
    "use strict";

    // var loadingScreen = require('website_utilities.loader').loadingScreen;
    var core = require('web.core');
    var time = require('web.time');

    $(function() {

        $('#upgradeModal').on('show.bs.modal', function(e) {
            var upgradeLine = $(e.relatedTarget).data('line-id');
            $(e.currentTarget).find('input[name="upgrade_line_id"]').val(upgradeLine);
        });

         $(document).on('click', '.upgrade-line', function () {
            var lineId = $(this).attr('data-line-id');
            var action = '/contract/get/' + lineId;
            $('#div_upgrade_line').html("");
            // loadingScreen();

            $.post(action, function (res) {
                var results = JSON.parse(res);
                $('#div_upgrade_line').html(results['line_html'] ? results['line_html'] : '');
            });
            // If user decides to manipulate id and task doesn't exist, unblock after 1 sec
            setTimeout(
                function () {
                    $.unblockUI();
                }, 1000
            );
        });

        // $(document).on('click', '.upgrade-confirm', function() {
        //     var lineValue = document.getElementsByName('upgrade_line_id')[0].value;
        //     var action = '/contract/line/upgrade/' + lineValue;
        //     $('#upgradeModal').modal('hide');
        //     $.get(action).done(function(data) {
        //         location.reload();
        //     });
        // });
    });
});
