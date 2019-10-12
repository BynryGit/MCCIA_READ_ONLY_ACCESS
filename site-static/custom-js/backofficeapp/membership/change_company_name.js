$(document).ready(function(){
    from_date=$('#from_date').val()
    to_date=$('#to_date').val()
    change_company_name_details_table(from_date,to_date);
});

function change_company_name_details_table(from_date,to_date){

    var table = $('#company_name_details');
        var oTable = table.dataTable({
            "processing": true,
            "serverSide": true,
            "destroy": true,
            "ajax": '/reportapp/change-company-name-details-datatable/?from_date='+from_date+"&to_date="+to_date,
            "searching": true,
            "Filter": true,
            "ordering": true,
            "serverSide": true,
            "paging": true,
            "columnDefs": [
                {"targets": 0, "orderable": false,"className": "text-center"},
                {"targets": 1, "orderable": false,"className": "text-center"},
                {"targets": 2, "orderable": false,"className": "text-left"},
                {"targets": 3, "orderable": false,"className": "text-left"},
            ],
            buttons: [
                { extend: 'print', className: 'btn dark btn-outline',
                    exportOptions: { columns: [0, 1, 2, 3] },
                },
                { extend: 'copy', className: 'btn red btn-outline',
                    exportOptions: { columns: [0, 1, 2, 3] },
                },
                { extend: 'pdf', className: 'btn green btn-outline',
                    exportOptions: { columns: [0, 1, 2, 3] },
                },
                { extend: 'excel', className: 'btn yellow btn-outline ',
                    exportOptions: { columns: [0, 1, 2, 3] },
                },
                { extend: 'csv', className: 'btn purple btn-outline ',
                    exportOptions: { columns: [0, 1, 2, 3] },
                },
                { extend: 'colvis', className: 'btn dark btn-outline', text: 'Columns'}
            ],

            responsive: false,

            "order": [[0, 'asc']],

            "lengthMenu": [ [10, 25, 50, 100, -1], [10, 25, 50, 100, "All"] ],

            "pageLength": 10,
        });
        $(".dataTables_filter").hide();

        $('#company_details_tools > li > a.tool-action').on('click', function() {
            var action = $(this).attr('data-action');
            $('#company_name_details').DataTable().button(action).trigger();
        });

        $("#search_company_details_text").keyup(function() {
            oTable.fnFilter($("#search_company_details_text").val());
        });
}

function change_company_name(){
    requested_value = $("#search_company_details_text").val();
    from_date=$('#from_date').val();
    to_date=$('#to_date').val();
    if (from_date == '' || to_date == ''){
        bootbox.alert("<span class='center-block text-center'>Please enter valid date</span>");
    }
    $.ajax({
        type : "GET",
        url : '/reportapp/download-company-name-details/?from_date='+from_date+'&to_date='+to_date,
        success : function(response){
            if(response.success == 'invalid_date'){
                        bootbox.alert("<span class='center-block text-center'>To date should be greater than or equal to from date</span>");
                    }
            if(response.success == 'true'){
                window.location.href = '/reportapp/change-company-name-excel/?from_date='+from_date+'&to_date='+to_date;
                clear_company();
            }
            else if(response.success == 'no data'){
               bootbox.alert("<span class='center-block text-center'>Data Is Not Present</span>");
            }
        },
        error : function(response){
            bootbox.alert("<span class='center-block text-center'>Something Went Wrong!</span>");
        }
    });
}


function clear_company(){
    document.getElementById("search_company_details_text").value = "";
    from_date=$('#from_date').val('');
    to_date=$('#to_date').val('');
    load_datatable();
    }
function load_datatable(){
    from_date=$('#from_date').val();
    to_date=$('#to_date').val();
    change_company_name_details_table(from_date,to_date);
}