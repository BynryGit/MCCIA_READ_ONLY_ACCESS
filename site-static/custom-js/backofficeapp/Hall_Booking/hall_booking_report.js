$("#hall_booking_anchor").addClass("tab-active");
$("#hall_booking_nav").addClass("active");
$("#hall_booking_icon").addClass("icon-active");
$("#hall_booking_active").css("display","block");

$(document).ready(function(){
       select_location = $("#select_location").val()
  	   select_hall = $("#select_hall").val()
  	   select_company = $("#select_company").val()
  	   select_payment = $("#select_payment").val()
  	   start_date = $("#from_date").val()
  	   end_date = $("#to_date").val()
 	   load_hall_reg_details(select_location,select_hall,select_company,select_payment,start_date,end_date);
});

function get_hall_list(){
    select_location = $("#select_location").val();
    $("#select_hall").html('');
    $("#select_hall").select2({data: [{id:"all", text: 'Select'}]});
    if(select_location != "" && select_location != "all"){
        $.ajax({
            type : "GET",
            url : '/backofficeapp/get-hall-list/',
            data : {'select_location':select_location},
            success: function (response) {
                if(response.success =='true'){
                    $.each(response.hall, function (index, item) {
                        $("#select_hall").append('<option value="'+item.hall_id+'">'+item.hall_name+'</option>')
                    });
                }
            },
            error : function(response){
                alert("_Error");
            }
        });
    }

}

function filter(){
       select_location = $("#select_location").val()
  	   select_hall = $("#select_hall").val()
  	   select_company = $("#select_company").val()
  	   select_payment = $("#select_payment").val()
  	   start_date = $("#from_date").val()
  	   end_date = $("#to_date").val()
 	   load_hall_reg_details(select_location,select_hall,select_company,select_payment,start_date,end_date);
}

function clear_filter() {
        $("#filter_div").load(" #filter_div");
        setTimeout(function () {
            $('.select2').select2();
            test();
            filter();
        }, 1000);
}
function test(){
var date_input=$('.dateField'); //our date input has the name "date"
		var container=$('.bootstrap-iso form').length>0 ? $('.bootstrap-iso form').parent() : "body";
		date_input.datepicker({
			format: 'dd/mm/yyyy',
			container: container,
			todayHighlight: true,
			autoclose: true,
		})
		}

 function load_hall_reg_details(select_location,select_hall,select_company,select_payment,start_date,end_date) {
 var table = $('#hallregtable');
var oTable = table.dataTable({
        "processing": true,
        "serverSide": true,
        "destroy": true,
        "ajax": "/backofficeapp/get-hall-regs-report-datatable/?select_location="+select_location+'&select_hall='+select_hall+'&select_company='+select_company+'&select_payment='+select_payment+"&start_date="+start_date+"&end_date="+end_date,
        "searching": true,
        "paging": true,
        "Filter": true,
        "ordering": true,
        "columnDefs": [
			{"targets": 0, "orderable": true, "className": "text-center"},
            {"targets": 1, "orderable": false},
            {"targets": 2, "orderable": false},
            {"targets": 3, "orderable": false},
            {"targets": 4, "orderable": false},
            {"targets": 5, "orderable": false, "className": "text-center"},
            {"targets": 6, "orderable": false, "className": "text-center"},
            {"targets": 7, "orderable": false, "className": "text-center"},
            {"targets": 8, "orderable": false, "className": "text-center"},
            {"targets": 9, "orderable": false, "className": "text-center"},
            {"targets": 10, "orderable": false, "className": "text-center"},
            {"targets": 11, "orderable": false, "className": "text-center"},
            {"targets": 12, "orderable": false, "className": "text-center"},
            {"targets": 13, "orderable": false, "className": "text-center"},
            {"targets": 14, "orderable": false, "className": "text-center"},
            {"targets": 15, "orderable": false, "className": "text-center"},
            {"targets": 16, "orderable": false, "className": "text-center"},
            {"targets": 17, "orderable": false, "className": "text-center"},
            {"targets": 18, "orderable": false, "className": "text-center"},
            {"targets": 19, "orderable": false, "className": "text-center"},
            {"targets": 20, "orderable": false, "className": "text-center"},
            {"targets": 21, "orderable": false, "className": "text-center"},
            {"targets": 22, "orderable": false, "className": "text-center"},
            {"targets": 23, "orderable": false, "className": "text-center"},
            {"targets": 24, "orderable": false, "className": "text-center"},
            {"targets": 25, "orderable": false, "className": "text-center"},
            {"targets": 26, "orderable": false, "className": "text-center"},
            {"targets": 27, "orderable": false, "className": "text-center"},
            {"targets": 28, "orderable": false, "className": "text-center"},

        ],
        buttons: [
            { extend: 'print', className: 'btn dark btn-outline' },
            { extend: 'copy', className: 'btn red btn-outline' },
            { extend: 'pdf', className: 'btn green btn-outline' },
            { extend: 'excel', className: 'btn yellow btn-outline ' },
            { extend: 'csv', className: 'btn purple btn-outline ' },
        ],
        // setup responsive extension: http://datatables.net/extensions/responsive/
        responsive: false,
        "order": [
            [1, 'asc']
        ],

        "lengthMenu": [
            // change per page values here
            [10, 20, 50,100,-1],
            [10, 20, 50,100,'All']
        ],
        // set the initial value
        "pageLength": 10,
    });

    $("#regSearch").keyup(function() {
        oTable.fnFilter($("#regSearch").val());
    });
    $('#hallregtable_tools > li > a.tool-action').on('click', function() {
        var action = $(this).attr('data-action');
        oTable.DataTable().button(action).trigger();
    });

}