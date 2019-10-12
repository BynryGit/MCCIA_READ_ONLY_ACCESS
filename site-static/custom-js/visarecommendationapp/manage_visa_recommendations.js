$("#visa_anchor").addClass("tab-active");
$("#visa_nav").addClass("active");
$("#visa_icon").addClass("icon-active");
$("#visa_active").css("display","block");


$(document).ready(function (){
 select_status = $("#select_status").val()
 select_location = $("#select_location").val()
 load_visa_table(select_status,select_location);
});

function change_status(){
 select_status = $("#select_status").val()
 select_location = $("#select_location").val()
 load_visa_table(select_status,select_location);
 }


function load_visa_table(select_status,select_location){
var oTable = $('#VisaListTable').dataTable({
	
				"processing": true,
            "serverSide": true,
            "destroy": true,
            "searching": true,
            "filtering": true,
            "ordering": true,

            "ajax": "/visarecommendationapp/get-visa-datatable/?select_status="+select_status+"&select_location="+select_location,
            "paging": true,
            "columnDefs": [
                {"targets": 1, "orderable": false, "className": "text-center"},
                {"targets": 2, "orderable": true, "className": "text-center"},
                {"targets": 3, "orderable": false, "className": "text-center"},
                {"targets": 4, "orderable": false, "className": "text-center"},
                {"targets": 5, "orderable": false, "className": "text-center"},
                {"targets": 6, "orderable": false, "className": "text-center"},
                {"targets": 7, "orderable": false, "className": "text-center"},
                {"targets": 8, "orderable": false, "className": "text-center"},
                {"targets": 9, "orderable": false, "className": "text-center"},
            ],
        // setup responsive extension: http://datatables.net/extensions/responsive/
            responsive: false,
            buttons: [
                {extend: 'print', className: 'btn dark btn-outline',
                    exportOptions: { columns: [0, 1, 2,3,4,5,6,7,8] },
                },
                {extend: 'copy', className: 'btn red btn-outline',
                    exportOptions: { columns: [0, 1, 2,3,4,5,6,7,8] },
                },
                {extend: 'pdf', className: 'btn green btn-outline',
                    exportOptions: { columns: [0, 1, 2,3,4,5,6,7,8] },
                },
                {extend: 'excel', className: 'btn yellow btn-outline',
                    exportOptions: { columns: [0, 1, 2,3,4,5,6,7,8] },
                },
                {extend: 'csv', className: 'btn purple btn-outline',
                    exportOptions: { columns: [0, 1, 2,3,4,5,6,7,8] },
                },
                {extend: 'colvis', className: 'btn dark btn-outline', text: 'Columns'}
            ],

        //"ordering": false, disable column ordering
        //"paging": false, disable pagination

            "order": [
                [2, 'desc']
            ],

            "lengthMenu": [
            // change per page values here
                 [10, 25, 50, 100],
                 [10, 25, 50, 100],
            ],
        // set the initial value
            "pageLength": 25,
        });
         $('#VisaListTable_tools > li > a.tool-action').on('click', function() {
            var action = $(this).attr('data-action');
            $('#VisaListTable').DataTable().button(action).trigger();
        });

        $("#txtSearch").keyup(function() {
            oTable.fnFilter($("#txtSearch").val());
        });
}

function update_visa_details(){
	 $("#second_footer").css("display", "none");
  	 $("#first_footer").css("display", "block");
	 var visa_approve_ids = [];
	 $('.check_approve:checkbox:checked').each(function () {
      visa_approve_ids.push($(this).val());
    });
  	 if (visa_approve_ids == '') {
  	 	   $("#second_footer").css("display", "block");
  	 	   $("#first_footer").css("display", "none");
  	 		$("#active_deactive_visa_text").html('').text('Please select request for approve');
  	 		return false;
  	 }
    $("#active_deactive_visa_text").html('').text('Do you want to approve Visa Request ?');
    $("#visa_id_list").val(visa_approve_ids);
}


toastr.options = {
  "closeButton": true,
  "debug": false,
  "positionClass": "toast-top-center",
  "onclick": null,
  "showDuration": "1000",
  "hideDuration": "1000",
  "timeOut": "5000",
  "extendedTimeOut": "1000",
  "showEasing": "swing",
  "hideEasing": "linear",
  "showMethod": "fadeIn",
  "hideMethod": "fadeOut"
}

function change_visa_details(){
    var visa_id_list = $("#visa_id_list").val();
    $.ajax({
        type: "GET",
        url: '/visarecommendationapp/update-visa-details/',
        data: {'visa_id_list': visa_id_list},
        success: function(response){
        	toastr.success("Approved Successfully");
        change_status();
        }
    });
}


