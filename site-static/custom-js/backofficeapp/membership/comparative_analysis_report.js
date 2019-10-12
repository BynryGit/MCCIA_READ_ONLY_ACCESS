$(document).ready(function(){
    comparative_analysis()
});

function comparative_analysis(){
    var table = $('#comparative_analysis_table');
        var oTable = table.dataTable({
            "processing": true,
            "serverSide": true,
            "destroy": true,
            "ajax": '/reportapp/comparative-analysis-datatable/',
            "searching": true,
            "Filter": true,
            "ordering": false,
            "serverSide": true,
            "paging": true,
            "columnDefs": [
                {"targets": 0, "orderable": true,"className": "text-center"},
                {"targets": 1, "orderable": false,"className": "text-center"},
                {"targets": 2, "orderable": false,"className": "text-center"},
                {"targets": 3, "orderable": false,"className": "text-center"},
                {"targets": 4, "orderable": false,"className": "text-center"},
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

        $('#comparative_report_tools > li > a.tool-action').on('click', function() {
            var action = $(this).attr('data-action');
            $('#comparative_analysis_table').DataTable().button(action).trigger();
        });

        $("#search_company_details_text").keyup(function() {
            oTable.fnFilter($("#search_company_details_text").val());
        });
}


function comparative_analysis_excel(){
    $.ajax({
        type : "GET",
        url : '/reportapp/download-comparative-analysis-excel/',
        success : function(response){
            
        },
        error : function(response){
        }
    });
    window.location.href = "/reportapp/download-comparative-analysis-excel/";
}