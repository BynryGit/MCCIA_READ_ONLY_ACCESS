$("#events_anchor").addClass("tab-active");
$("#events_nav").addClass("active");
$("#events_icon").addClass("icon-active");
$("#events_active").css("display","block");

$(document).ready(function(){
        select_committee = $("#select_committee").val()
  	   select_event = $("#select_event").val()
  	   select_payment = $("#select_payment").val()
  	   start_date = $("#from_date").val()
  	   end_date = $("#to_date").val()
 	   load_events_details(select_committee,select_event,select_payment,start_date,end_date);
});

function filter(){
       select_committee = $("#select_committee").val()
  	   select_event = $("#select_event").val()
  	   select_payment = $("#select_payment").val()
  	   start_date = $("#from_date").val()
  	   end_date = $("#to_date").val()
 	   load_events_details(select_committee,select_event,select_payment,start_date,end_date);
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

 function load_events_details(select_committee,select_event,select_payment,start_date,end_date) {
 var table = $('#EventListTable');
var oTable = table.dataTable({
        //"processing": true,
        "serverSide": true,
        "destroy": true,
        "ajax": "/backofficeapp/get-events-report-datatable/?select_committee="+select_committee+'&select_event='+select_event+'&select_payment='+select_payment+"&start_date="+start_date+"&end_date="+end_date,
        "searching": false,
        "paging": true,
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

        ],
        buttons: [
            { extend: 'print', className: 'btn dark btn-outline' },
            { extend: 'copy', className: 'btn red btn-outline' },
            { extend: 'pdf', className: 'btn green btn-outline' },
            { extend: 'excel', className: 'btn yellow btn-outline ' },
            { extend: 'csv', className: 'btn purple btn-outline ' },
            { extend: 'colvis', className: 'btn dark btn-outline', text: 'Columns'}
        ],

        // setup responsive extension: http://datatables.net/extensions/responsive/
        responsive: false,

        //"ordering": false, disable column ordering
        //"paging": false, disable pagination

        "order": [
            [1, 'asc']
        ],

        "lengthMenu": [
            // change per page values here
            [10, 20, 50],
            [10, 20, 50]
        ],
        // set the initial value
        "pageLength": 10,
    });

    $("#slabSearch").keyup(function() {
        oTable.fnFilter($("#slabSearch").val());
    });

    // handle datatable custom tools

    $('#slab_details_tools > li > a.tool-action').on('click', function() {
        var action = $(this).attr('data-action');
        oTable.DataTable().button(action).trigger();
    });

}