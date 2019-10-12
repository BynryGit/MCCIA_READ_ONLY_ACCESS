
$(document).ready(function(e){
    $("#awards_anchor").addClass("tab-active");
    $("#awards_nav").addClass("active");
    $("#awards_icon").addClass("icon-active");
    $("#awards_active").css("display","block");
    $("#awards_nav").addClass("active");

    filter_award();
});


// Filter Award Registration Table
function filter_award(){
    var award_id = $("#award").val();
    get_award_registration_table(award_id);
}


// Get Award Registration Datable
function get_award_registration_table(award_id){
    var url = '/backofficeapp/get-award-registration-datatable/?award_id='+award_id;
    var table = $('#award_registration_table');
    var oTable = table.dataTable({
        "processing": true,
        "serverSide": true,
        "destroy": true,
        "ajax": url,
        "searching": true,
        "Filter": true,
        "ordering": false,
        "paging": true,
        "columnDefs": [
            {"targets": [0,1,2,3], "orderable": false},
        ],
        buttons: [
            {extend: 'print', className: 'btn dark btn-outline',
                exportOptions: { columns: [0,1,2] },
            },
            {extend: 'copy', className: 'btn red btn-outline',
                exportOptions: { columns: [0,1,2] },
            },
            {extend: 'pdf', className: 'btn green btn-outline',
                exportOptions: { columns: [0,1,2] },
            },
            {extend: 'excel', className: 'btn yellow btn-outline',
                exportOptions: { columns: [0,1,2] },
            },
            {extend: 'csv', className: 'btn purple btn-outline',
                exportOptions: { columns: [0,1,2] },
            },
            {extend: 'colvis', className: 'btn dark btn-outline', text: 'Columns'}
        ],

        responsive: false,

        "order": [[0, 'asc']],

        "lengthMenu": [ [10, 25, 50, 100, -1], [10, 25, 50, 100, "All"] ],

        "pageLength": 10,
    });

    $(".dataTables_filter").hide();

//    $("#search_member_detail_text").keyup(function() {
//        if ($("#search_member_detail_text").val().length >= 4){
//            oTable.fnFilter($("#search_member_detail_text").val());
//        }
//    });

    $('#award_registration_table_tools > li > a.tool-action').on('click', function() {
        var action = $(this).attr('data-action');
        oTable.DataTable().button(action).trigger();
    });
}


// Clear Award Filter
function clear_awards(){
	$("#award").val("All").trigger('change');
	filter_award();
}


// Download Award Excel Report
function download_award(){
    var award_id = $("#award").val();
    var url = '/backofficeapp/download-award-data/'+award_id;
    window.open(url, '_blank');
}