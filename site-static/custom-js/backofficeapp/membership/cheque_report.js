$(document).ready(function(){
    from_date = $('#from_date').val()
    to_date = $('#to_date').val()
    status = $('#payment_status').val()
    cheque_details_datatable(from_date,to_date,status);
});

    $("#member_anchor").addClass("tab-active");
    $("#member_nav").addClass("active");
    $("#member_icon").addClass("icon-active");
    $("#member_active").css("display", "block");
    $(".sel2").select2({
        width: '100%'
    })

// TODO datatable
function cheque_details_datatable(from_date,to_date,status){
    var table = $('#bouncecheque_details_table');
        var oTable = table.dataTable({
            "processing": true,
            "serverSide": true,
            "destroy": true,
            "ajax": '/reportapp/bounce-cheque-details-datatable/?from_date='+from_date+"&to_date="+to_date+"&status="+status,
            "searching": true,
            "Filter": true,
            "ordering": false,
            "serverSide": true,
            "paging": true,
            "columnDefs": [
                {"targets": 0, "orderable": false,"className": "text-center"},
                {"targets": 1, "orderable": true,"className": "text-center"},
                {"targets": 2, "orderable": false,"className": "text-center"},
                {"targets": 3, "orderable": false,"className": "text-left"},
                {"targets": 4, "orderable": false,"className": "text-center"},
                {"targets": 5, "orderable": false,"className": "text-center"},
                {"targets": 6, "orderable": false,"className": "text-left"},
                {"targets": 7, "orderable": false,"className": "text-center"},
                {"targets": 8, "orderable": false,"className": "text-center"}
            ],
            buttons: [
                { extend: 'print', className: 'btn dark btn-outline',
                    exportOptions: { columns: [0, 1, 2, 3, 4, 5, 6, 7, 8] },
                },
                { extend: 'copy', className: 'btn red btn-outline',
                    exportOptions: { columns: [0, 1, 2, 3, 4, 5, 6, 7, 8] },
                },
                { extend: 'pdf', className: 'btn green btn-outline',
                    exportOptions: { columns: [0, 1, 2, 3, 4, 5, 6, 7, 8] },
                },
                { extend: 'excel', className: 'btn yellow btn-outline ',
                    exportOptions: { columns: [0, 1, 2, 3, 4, 5, 6, 7, 8] },
                },
                { extend: 'csv', className: 'btn purple btn-outline ',
                    exportOptions: { columns: [0, 1, 2, 3, 4, 5, 6, 7, 8] },
                },
                { extend: 'colvis', className: 'btn dark btn-outline', text: 'Columns'}
            ],

            responsive: false,

            "order": [[1, 'asc']],

            "lengthMenu": [ [10, 25, 50, 100, -1], [10, 25, 50, 100, "All"] ],

            "pageLength": 10,
        });
        $(".dataTables_filter").hide();

        $('#bouncecheque_details_table_tools > li > a.tool-action').on('click', function() {
            var action = $(this).attr('data-action');
            $('#bouncecheque_details_table').DataTable().button(action).trigger();
        });

        $("#search_cheque_details_text").keyup(function() {
            oTable.fnFilter($("#search_cheque_details_text").val());
        });
}

// TODO download button
function download_cheque_details(){
    requested_value = $("#search_cheque_details_text").val();
    from_date=$('#from_date').val();
    to_date=$('#to_date').val();
    payment_status = $("#payment_status").val();
    if (from_date == '' || to_date == ''){
        bootbox.alert("<span class='center-block text-center'>Please enter valid date</span>");
    }
    $.ajax({
        type : "GET",
        url : "/reportapp/download-cheque-details/?from_date="+from_date+'&to_date='+to_date+'&payment_status='+payment_status,
        data : {
            'from_date' : from_date,
            'to_date' : to_date
        },
        success : function(response){
            if(response.success == 'true'){
                window.location.href = '/reportapp/downloadcheque-detail-excel/?from_date='+from_date+'&to_date='+to_date+'&payment_status='+payment_status;
                $('#search_cheque_details_text').val('');
                from_date=$('#from_date').val('');
                to_date=$('#to_date').val('');
                status = $('#payment_status').val('not_paid').change();
                clear_values();
            }
            else {
                    if(response.success == 'no data'){
                        bootbox.alert("<span class='center-block text-center'>No Data Available</span>");
                    }
                    if(response.success == 'invalid_date'){
                        bootbox.alert("<span class='center-block text-center'>To date should be greater than or equal to from date</span>");
                    }
            }
        },
        error : function(response){
            bootbox.alert("<span class='center-block text-center'>Something Went Wrong!</span>");
        }
    });
}

// TODO filter button
function clear_datatable_filter(){
    $('#search_cheque_details_text').val('');
    from_date=$('#from_date').val('');
    to_date=$('#to_date').val('');
    status = $('#payment_status').val('not_paid').change()
    clear_values();
}

// TODO filter button
function filter_cheqe_datatable(){
    from_date=$('#from_date').val();
    to_date=$('#to_date').val();
    status = $('#payment_status').val()
    if (from_date == '' && to_date == '' && status == ''){
        bootbox.alert("<span class='center-block text-center'>Please enter valid date</span>");
    }
    cheque_details_datatable(from_date,to_date,status);
}

//  TODO clear button
function clear_values(){
    from_date=$('#from_date').val();
    to_date=$('#to_date').val();
    status = $('#payment_status').val()
    cheque_details_datatable(from_date,to_date,status);
}