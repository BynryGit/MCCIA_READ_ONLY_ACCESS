$(document).ready(function () {
  request_membership_schedule_upload_table();
});


function clear_membership_schedule_file() {
    $("#upload_membership_schedule_file").val('');
}


function upload_membership_schedule_file(){
var flag=true

if ($('#upload_membership_schedule_file').val() == ''){
    flag=false
    $("#error_membership_schedule_file").addClass('has-error')
    }

    var input = document.getElementById("upload_membership_schedule_file");
    membership_schedule_file = input.files[0];

    var formData= new FormData();
    formData.append("membership_schedule_file",membership_schedule_file);

if (flag){
    $.ajax({
        type:'POST',
        url:'/backofficeapp/upload-membership-schedule-file/',
        data: formData,
        cache: false,
        processData: false,
        contentType: false,
        success: function(response) {
            if (response.success == "true") {
                alert("Membership Schedule uploaded Successfully")
                window.location.href = "/backofficeapp/upload-membership-schedule-landing";
                clear_membership_schedule_file()
            }
        },
        error:function (response){
            bootbox.alert("<span class='center-block text-center'>Data is not Stored. Please enter valid data.</span>");
        },
        beforeSend: function() {
        $('#processing').show();
        },
        complete: function() {
        $('#processing').hide();
        }
    });
    }
else{
    return false
    }
}


function request_membership_schedule_upload_table(){
    var table = $('#upload_membership_schedule_table');
    var oTable = table.dataTable({
        "processing": true,
        "serverSide": true,
        "destroy": true,
        "ajax": '/backofficeapp/get-membership-schedule-datatable/',
        "searching": true,
        "Filter": true,
        "ordering": false,
        "paging": true,
        "columnDefs": [
            {"className": "dt-center","targets": 0, "orderable": false},
            {"className": "dt-center","targets": 1, "orderable": false},
            {"className": "dt-left", "targets": 2, "orderable": false},
            {"className": "dt-left", "targets": 3, "orderable": false},

        ],
        buttons: [
            {extend: 'print', className: 'btn dark btn-outline',
                exportOptions: { columns: [0, 1, 2,3] },
            },
            {extend: 'copy', className: 'btn red btn-outline',
                exportOptions: { columns: [0, 1, 2] },
            },
            {extend: 'pdf',className: 'btn green btn-outline',
                exportOptions: { columns: [0, 1, 2] },
            },
            {extend: 'excel',className: 'btn yellow btn-outline',
                exportOptions: { columns: [0, 1, 2] },
            },
            {extend: 'csv',className: 'btn purple btn-outline',
                exportOptions: { columns: [0, 1, 2] },
            },
            {extend: 'colvis',className: 'btn dark btn-outline',text: 'Columns'}
        ],

        responsive: false,

        "order": [
            [0, 'asc']
        ],

        "lengthMenu": [ [10, 25, 50, 100, -1], [10, 25, 50, 100, "All"] ],

        "pageLength": 10,
    });

    $(".dataTables_filter").hide();

    $("#search_legal_detail_text").keyup(function() {
        oTable.fnFilter($("#search_legal_detail_text").val());
    });

    $('#legal_details_tools > li > a.tool-action').on('click', function() {
        var action = $(this).attr('data-action');
        $('#legal_details').DataTable().button(action).trigger();
    });
}




