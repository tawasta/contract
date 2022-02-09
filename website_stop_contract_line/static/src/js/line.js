odoo.define('website_stop_contract_line.portal_contract_page', function (require) {
    "use strict";

    $(function() {

        $('#cancelModal').on('show.bs.modal', function(e) {
            var removeLine = $(e.relatedTarget).data('line-id');
            $(e.currentTarget).find('input[name="stop_line_id"]').val(removeLine);
        });

        $(document).on('click', '.stop-confirm', function() {
            var lineValue = document.getElementsByName('stop_line_id')[0].value;
            var action = '/contract/line/stop/' + lineValue;
            $('#cancelModal').modal('hide');
            $.get(action).done(function(data) {
                location.reload();
            });
        });
    });
});
