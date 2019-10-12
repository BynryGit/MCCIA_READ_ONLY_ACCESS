
$("#member_anchor").addClass("tab-active");
$("#member_nav").addClass("active");
$("#member_icon").addClass("icon-active");
$("#member_active").css("display","block");
$("#member_nav").addClass("active");


$(".sel2").select2({
            width: '100%'
        })

$(document).ready(function(){
    var select_invoice_for = 'show_all';
    request_proforma_datatable(select_invoice_for)


});

<!--function color_it(){-->
    <!--$('#certificate_send_mail_table > tbody  > tr').each(function() {-->
        <!--$(this).css('background-color','green');-->
    <!--});-->
<!--}-->

    function request_proforma_datatable(select_invoice_for,acceptance_from,acceptance_to){
        var acceptance_from = $("#acceptance_from").val();
        var acceptance_to = $("#acceptance_to").val();
        var table = $('#certificate_send_mail_table');
        var oTable = table.dataTable({
            "processing": true,
            "serverSide": true,
            "destroy": true,
            "ajax": '/backofficeapp/get-bulk-mail-certificate-table/?select_invoice_for='+select_invoice_for+'&acceptance_from='+acceptance_from+'&acceptance_to='+acceptance_to,
            "searching": true,
            "Filter": true,
            "ordering": false,
            "paging": true,
            "columnDefs": [
                {"className": "dt-center","targets": 0, "orderable": false},
                {"className": "dt-center","targets": 1, "orderable": false},
                {"className": "dt-left", "targets": 2, "orderable": false},
                {"className": "dt-center","targets": 3, "orderable": false},
                {"className": "dt-center","targets": 4, "orderable": false},
                {"className": 'select-checkbox', "targets":   5, "defaultContent": '',},


            ],
            select: {
                style:    'os',
                selector: 'td:last-child'
            },
            buttons: [
                {extend: 'print', className: 'btn dark btn-outline',
                    exportOptions: { columns: [0, 1, 2, 3] },
                },
                {extend: 'copy', className: 'btn red btn-outline',
                    exportOptions: { columns: [0, 1, 2, 3] },
                },
                {extend: 'pdf',className: 'btn green btn-outline',
                    exportOptions: { columns: [0, 1, 2, 3] },
                },
                {extend: 'excel',className: 'btn yellow btn-outline',
                    exportOptions: { columns: [0, 1, 2, 3] },
                },
                {extend: 'csv',className: 'btn purple btn-outline',
                    exportOptions: { columns: [0, 1, 2, 3] },
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

            $('#certificate_send_mail_table_tools > li > a.tool-action').on('click', function() {
            var action = $(this).attr('data-action');
            $('#certificate_send_mail_table').DataTable().button(action).trigger();
            });

            $("#search_company").keyup(function() {
            oTable.fnFilter($("#search_company").val());
    });


    }
    function filter_company_table(){
        var select_invoice_for = $("#select_invoice_for").val();
        request_proforma_datatable(select_invoice_for);
    }


function send_email(){
      var sent_user_mail_ids = [];
    $('.check_user:checkbox:checked').each(function () {
        sent_user_mail_ids.push($(this).val());
    });


        $.ajax({
        type: "GET",
        url: '/backofficeapp/create-schedule-job-for-mail/',
        data: {'sent_user_mail_ids':sent_user_mail_ids},
        success: function(response){
            if (response.success == 'true'){
                bootbox.confirm("Are you sure you want to create Schedule.", function(result){
                console.log('This was logged in the callback: ' + result);
                 });

               bootbox.alert("<span class='center-block text-center'>Job Schedule successfully</span>",function(){
                   			 location.href = '/backofficeapp/send-certificate-bulk-mail/'
                   	});
            }
            else{
            bootbox.alert("<span class='center-block text-center'>Sorry Error Ocured</span>",function(){
                   			 location.href = '/backofficeapp/send-certificate-bulk-mail/'
                   	});
            }
        }
        });
    };


function select_unselect_checkbox(ele) {
     var checkboxes = document.getElementsByTagName('input');
     if (ele.checked) {
         for (var i = 0; i < checkboxes.length; i++) {
             console.log(i)
             if (checkboxes[i].type == 'checkbox') {
                 checkboxes[i].checked = true;
             }
         }
     } else {
         for (var i = 0; i < checkboxes.length; i++) {
             console.log(i)
             if (checkboxes[i].type == 'checkbox') {
                 checkboxes[i].checked = false;
             }
         }
     }
 }



