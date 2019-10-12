
	
	function call_prev(page_number){
	
	call_href = window.location.href
	var lastChar = call_href.substr(call_href.length - 1);
	if(lastChar == '/'){
	  call_href = call_href+"?page="+page_number
	  }
	else{
	  call_href = call_href+"&page="+page_number
	  }
	  window.location=call_href
	}
	
	function call_next(page_number){
	
	call_href = window.location.href
	var lastChar = call_href.substr(call_href.length - 1);
	if(lastChar == '/'){
	  call_href = call_href+"?page="+page_number
	 }
	else{
	   call_href = call_href+"&page="+page_number
	  }
	  window.location=call_href
	}
	    
	    $("#country1").change(function () {
	        getState1();
	    });
	    $("#statec1").change(function () {
	        getCity1();
	    });
	
	    function getState1() {
	        $("#subscriber_div").css("display","none");
	
	        country_id = $('#country1 :selected').val();
	        if (country_id) {
	            $.ajax({
	                type: 'GET',
	                url: '/get-state/',
	                data: {'country_id': country_id},
	                success: function (response) {
							  if (response.success == 'Expired') {		
						  			location.href = '/backoffice/?status=Expired'
						  		}                  
	                    $('#statec1').html('');
	                    $('#statec1').append("<option value=''>Select State</option>");
	                    $.each(response.state_list, function (index, item) {
	                        $('#statec1').append(item);
	                    });
	                    $('#statec1').val("").change();
	                    $('#currency').val(response.currency)
	                },
	                error: function (response) {
	                    alert("Error!");
	                },
	            });
	        }
	        else {
	            $('#statec1').html('');
	            $('#statec1').append("<option value=''>Select State</option>");
	            $('#statec1').val("").change();
	        }
	    }
	
	    function getCity1() {
	        $("#subscriber_div").css("display","none");
	
	        state_id = $('#statec1 :selected').val();
	        if (state_id) {
	            $.ajax({
	                type: 'GET',
	                url: '/get-city-place/',
	                data: {'state_id': state_id},
	                success: function (response) {
							  if (response.success == 'Expired') {		
						  			location.href = '/backoffice/?status=Expired'
						  		}                    
	                    //alert('success');
	                    $('#city1').html('');
	                    $('#city1').append("<option value=''>Select City</option>");
	                    $.each(response.city_list, function (index, item) {
	                        $('#city1').append(item);
	                    });
	                    $('#city1').val("").change();
	                },
	                error: function (response) {
	                    alert("Error!");
	                },
	            });
	        }
	        else {
	            $('#city1').html('');
	            $('#city1').append("<option value=''>Select City</option>");
	            $('#city1').val("").change();
	        }
	    }
	            
	    $("#supplier_anchor").addClass("tab-active");
	    $("#supplier_icon").addClass("icon-active");
	    $("#supplier_active").css("display","block");
	    
	    $(document).ready(function(){
	
	      if ({{flag_ck}} == 0) {      
	     		   $("#no_data").css("display","none");
	       }
	      else if({{cityfg}} == '0') {
	      	  $("#no_city").css("display","block");
	      }
	      else {
	
	      	  $("#no_city").css("display","none");
	     	     $("#no_data").css("display","block");
	      }
	         var maxHeight = 0;
	         var maxHeader = 0;
	
	        $('.prem_div1').each(function() {
	        maxHeight = Math.max(maxHeight, $(this).height());
	        maxHeight = maxHeight ;
	    }).height(maxHeight);
	    
	        $('.prem_div').each(function() {
	        maxHeight = Math.max(maxHeight, $(this).height());
	        maxHeight = maxHeight - 25;
	    }).height(maxHeight);
	    
	        $('.header_div').each(function() {
	        maxHeader = Math.max(maxHeader, $(this).height());
	        maxHeader = maxHeader - 3; 
	    }).height(maxHeader);
	    
	      $("#startDate").hide();
	    	$("#endDate").hide();
	      $(".sel2").select2({});
	      $("#city_id").select2({
	      width: '100%'
	     });
	    $("#startDate").datepicker({
	            
	        dateFormat: 'dd/mm/yy'
	    });
	    
	    $("#endDate").datepicker({
	            
	        dateFormat: 'dd/mm/yy'
	    });   
	    
	     $.datepicker._clearDate(this);
	    
	});
	
	flag =0;
	
	
	function filter_advert() {
	 sort_by = $('#sortby').val()
	 country_var = $('#country1').val()
	 state_var = $('#statec1').val()
	 city_name_var = $('#city1').val()
	   	 
			//checkCity
		/*	var city_status =checkCity()
			if (city_status == false){
					
					return false;		
			}*/
	
		   if (flag == 1){ 
			var ck_status =check_date_range()
			 isValid = false;
				if (ck_status == false){			
					return false;		
			}
			}
		
		if($('#startDate1').val() == ""){
	
		 startDate_var = $('#startDate').val()
	    endDate_var = $('#endDate').val()
	    //city_name_var = $('#city_id').val()
	    stat_var = $("input[name='stat']:checked").val()
		
		}else{
		
			    startDate_var = $('#startDate1').val()
	    endDate_var = $('#endDate').val()
	    //city_name_var = $('#city_id').val()
	    stat_var = $("input[name='stat']:checked").val()
		
		
		}
	
	    startDate_var = $('#startDate').val()
	    endDate_var = $('#endDate').val()
	    //city_name_var = $('#city_id').val()
	    stat_var = $("input[name='stat']:checked").val()
	    
		if(stat_var == undefined){
				stat_var = ""
		}
	
	    location.href = '/view-subscriber-list/?start_date_var='+startDate_var+'&end_date_var='+endDate_var+'&status_var='+stat_var+'&city_var='+city_name_var+'&country_var='+country_var+'&state_var='+state_var+'&sort_by='+sort_by
	}
	
	$('#date_range').on('click', function() {
	flag=1
	
	});
	
	function check_date_range(){
	
	  
	        if(check_start_date() & check_end_date() )
	        {
	            return true;
	        }else{
	     
					return false;
				}
			
	}
	
	function check_start_date(){
	            var isValid = false;
	                if($("#startDate").val() ==""  || $("#startDate").val()== null)
	                {
	
	                    $("#startDate").parent().children('.error').css("display", "block");
	                    $("#startDate").parent().children('.error').text("Please select Start Date ");
	                  isValid = false;
	               }else{
	
	                    $("#startDate").parent().children('.error').css("display", "none");
	                isValid =  true;
	               }
	               return isValid;
	
	        }
	        
	 function check_end_date(){
	            var isValid = false;
	                if($("#endDate").val() ==""  || $("#endDate").val()== null)
	                {
	                    $("#endDate").parent().children('.error').css("display", "block");
	                    $("#endDate").parent().children('.error').text("Please select End Date ");
	                  isValid = false;
	               }else{
	
	                    $("#endDate").parent().children('.error').css("display", "none");
	                isValid =  true;
	               }
	               return isValid;
	        }
	        
	        function checkCity(){
	
	            city1 = $("#city_id").val();
	
	             if(city1 == '' || city1 == null)
	            {
	            $("#city_id").parent().children('.error').css("display", "block");
	             $("#city_id").parent().children('.error').text("Please select City");
	            return false;
	            }
	           else{
	            $("#city_id").parent().children('.error').css("display", "none");
	           return true;
	           }
	        }
	    
	
	function sort_by(){
	 sortby = $("#sortby").val();
	 country_var = $('#country1').val()
	 state_var = $('#statec1').val()
	 city_name_var = $('#city1').val()
	
	   if (city_name_var != '') {
	   location.href = '/view-subscriber-list/?city_var='+city_name_var+'&sort_by='+sortby+'&country_var='+country_var+'&state_var='+state_var	
	   }
	   else {
	   	return false;
	   }
	}
	
	    var date_flag = "1";
	
	    $("#One_week").click(function() {
	
	    $('#One_week').css({
	        'background-color': '#32C5D2',
	      'color': '#FFF',
	       
	    });
	    
	       $('#date_range').css({
		'background-color': '#FFF',
	   'border-color': '#32C5D2;',
	   'color': '#32C5D2;',
	   ' background': 'transparent none repeat scroll 0px 0px;'
	    });
	
	    $('#Six_month').css({
		'background-color': '#FFF',
	   'border-color': '#32C5D2;',
	   'color': '#32C5D2;',
	   ' background': 'transparent none repeat scroll 0px 0px;'
	    });
	        $('#One_month').css({
		'background-color': '#FFF',
	   'border-color': '#32C5D2;',
	   'color': '#32C5D2;',
	   ' background': 'transparent none repeat scroll 0px 0px;'
	    });
	        $('#Three_month').css({
		'background-color': '#FFF',
	   'border-color': '#32C5D2;',
	   'color': '#32C5D2;',
	   ' background': 'transparent none repeat scroll 0px 0px;'
	    });
	
	    	$("#startDate").hide();
	    	$("#endDate").hide();
	    	$("#startDate1").show();
	    	$("#endDate1").show();
	    	
	        var date = new Date();
	        date.setDate(date.getDate() - 7 );
	        var yyyy = date.getFullYear().toString();
	        var mm = (date.getMonth()+1).toString(); // getMonth() is zero-based
	        var dd  = date.getDate().toString();
	        newdate = (dd[1]?dd:"0"+dd[0]) + "/"+  (mm[1]?mm:"0"+mm[0]) + "/" +  yyyy;
	        $("#startDate").val(newdate);
	        $("#startDate1").val(newdate);
	        var date = new Date();
	        var yyyy = date.getFullYear().toString();
	        var mm = (date.getMonth()+1).toString(); // getMonth() is zero-based
	        var dd  = date.getDate().toString();
	        newdate = (dd[1]?dd:"0"+dd[0]) + "/"+  (mm[1]?mm:"0"+mm[0]) + "/" +  yyyy;
	        $("#endDate").val(newdate);
	        $("#endDate1").val(newdate);
	    });
	    $("#One_month").click(function() {
		
			    $('#One_month').css({
	        'background-color': '#32C5D2',
	      'color': '#FFF',
	       
	    });    
	    
	       $('#date_range').css({
		'background-color': '#FFF',
	   'border-color': '#32C5D2;',
	   'color': '#32C5D2;',
	   ' background': 'transparent none repeat scroll 0px 0px;'
	    });
	
	    $('#Six_month').css({
		'background-color': '#FFF',
	   'border-color': '#32C5D2;',
	   'color': '#32C5D2;',
	   ' background': 'transparent none repeat scroll 0px 0px;'
	    });
	        $('#Three_month').css({
		'background-color': '#FFF',
	   'border-color': '#32C5D2;',
	   'color': '#32C5D2;',
	   ' background': 'transparent none repeat scroll 0px 0px;'
	    });
	        $('#One_week').css({
		'background-color': '#FFF',
	   'border-color': '#32C5D2;',
	   'color': '#32C5D2;',
	   ' background': 'transparent none repeat scroll 0px 0px;'
	    });
	    
	        	$("#startDate").hide();
	    	$("#endDate").hide();
	    	$("#startDate1").show();
	    	$("#endDate1").show();
	        var date = new Date();
	        date.setDate(date.getDate() - 30 );
	        var yyyy = date.getFullYear().toString();
	        var mm = (date.getMonth()+1).toString(); // getMonth() is zero-based
	        var dd  = date.getDate().toString();
	        newdate = (dd[1]?dd:"0"+dd[0]) + "/"+  (mm[1]?mm:"0"+mm[0]) + "/" +  yyyy;
	        $("#startDate").val(newdate);
	         $("#startDate1").val(newdate);
	        var date = new Date();
	        var yyyy = date.getFullYear().toString();
	        var mm = (date.getMonth()+1).toString(); // getMonth() is zero-based
	        var dd  = date.getDate().toString();
	        newdate = (dd[1]?dd:"0"+dd[0]) + "/"+  (mm[1]?mm:"0"+mm[0]) + "/" +  yyyy;
	        $("#endDate").val(newdate);
	         $("#endDate1").val(newdate);
	    });
	    $("#Three_month").click(function() {
	    
	    				    $('#Three_month').css({
	        'background-color': '#32C5D2',
	      'color': '#FFF',
	       
	    }); 
	    
	       $('#date_range').css({
		'background-color': '#FFF',
	   'border-color': '#32C5D2;',
	   'color': '#32C5D2;',
	   ' background': 'transparent none repeat scroll 0px 0px;'
	    });
	
	    $('#Six_month').css({
		'background-color': '#FFF',
	   'border-color': '#32C5D2;',
	   'color': '#32C5D2;',
	   ' background': 'transparent none repeat scroll 0px 0px;'
	    });
	        $('#One_month').css({
		'background-color': '#FFF',
	   'border-color': '#32C5D2;',
	   'color': '#32C5D2;',
	   ' background': 'transparent none repeat scroll 0px 0px;'
	    });
	        $('#One_week').css({
		'background-color': '#FFF',
	   'border-color': '#32C5D2;',
	   'color': '#32C5D2;',
	   ' background': 'transparent none repeat scroll 0px 0px;'
	    });
	       
		
	   
	    
	        	$("#startDate").hide();
	    	$("#endDate").hide();
	    	$("#startDate1").show();
	    	$("#endDate1").show();
	        var date = new Date();
	        date.setDate(date.getDate() - 90 );
	        var yyyy = date.getFullYear().toString();
	        var mm = (date.getMonth()+1).toString(); // getMonth() is zero-based
	        var dd  = date.getDate().toString();
	        newdate = (dd[1]?dd:"0"+dd[0]) + "/"+  (mm[1]?mm:"0"+mm[0]) + "/" +  yyyy;
	        $("#startDate").val(newdate);
	        $("#startDate1").val(newdate);
	        var date = new Date();
	        var yyyy = date.getFullYear().toString();
	        var mm = (date.getMonth()+1).toString(); // getMonth() is zero-based
	        var dd  = date.getDate().toString();
	        newdate = (dd[1]?dd:"0"+dd[0]) + "/"+  (mm[1]?mm:"0"+mm[0]) + "/" +  yyyy;
	        $("#endDate").val(newdate);
	         $("#endDate1").val(newdate);
	    });
	    $("#Six_month").click(function() {
	    
	    				    $('#Six_month').css({
	        'background-color': '#32C5D2',
	      'color': '#FFF',
	       
	    });
	    
	        $('#date_range').css({
		'background-color': '#FFF',
	   'border-color': '#32C5D2;',
	   'color': '#32C5D2;',
	   ' background': 'transparent none repeat scroll 0px 0px;'
	    });
	
	    $('#Three_month').css({
		'background-color': '#FFF',
	   'border-color': '#32C5D2;',
	   'color': '#32C5D2;',
	   ' background': 'transparent none repeat scroll 0px 0px;'
	    });
	        $('#One_month').css({
		'background-color': '#FFF',
	   'border-color': '#32C5D2;',
	   'color': '#32C5D2;',
	   ' background': 'transparent none repeat scroll 0px 0px;'
	    });
	        $('#One_week').css({
		'background-color': '#FFF',
	   'border-color': '#32C5D2;',
	   'color': '#32C5D2;',
	   ' background': 'transparent none repeat scroll 0px 0px;'
	    });
	       
	    
	        	$("#startDate").hide();
	    	$("#endDate").hide();
	    	$("#startDate1").show();
	    	$("#endDate1").show();
	        var date = new Date();
	        date.setDate(date.getDate() - 180 );
	        var yyyy = date.getFullYear().toString();
	        var mm = (date.getMonth()+1).toString(); // getMonth() is zero-based
	        var dd  = date.getDate().toString();
	        newdate = (dd[1]?dd:"0"+dd[0]) + "/"+  (mm[1]?mm:"0"+mm[0]) + "/" +  yyyy;
	        $("#startDate").val(newdate);
	        $("#startDate1").val(newdate);
	        var date = new Date();
	        var yyyy = date.getFullYear().toString();
	        var mm = (date.getMonth()+1).toString(); // getMonth() is zero-based
	        var dd  = date.getDate().toString();
	        newdate = (dd[1]?dd:"0"+dd[0]) + "/"+  (mm[1]?mm:"0"+mm[0]) + "/" +  yyyy;
	        $("#endDate").val(newdate);
	         $("#endDate1").val(newdate);
	    });
	    
	    
	    $("#date_range").click(function() {
	
		    $('#date_range').css({
	        'background-color': '#32C5D2',
	      'color': '#FFF',
	
	    });
	      
	    $('#Six_month').css({
		'background-color': '#FFF',
	   'border-color': '#32C5D2;',
	   'color': '#32C5D2;',
	   ' background': 'transparent none repeat scroll 0px 0px;'
	    });
	
	    $('#Three_month').css({
		'background-color': '#FFF',
	   'border-color': '#32C5D2;',
	   'color': '#32C5D2;',
	   ' background': 'transparent none repeat scroll 0px 0px;'
	    });
	        $('#One_month').css({
		'background-color': '#FFF',
	   'border-color': '#32C5D2;',
	   'color': '#32C5D2;',
	   ' background': 'transparent none repeat scroll 0px 0px;'
	    });
	        $('#One_week').css({
		'background-color': '#FFF',
	   'border-color': '#32C5D2;',
	   'color': '#32C5D2;',
	   ' background': 'transparent none repeat scroll 0px 0px;'
	    });
	    
	      $("#startDate").show();
	    	$("#endDate").show();
	    	$("#startDate1").hide();
	    	$("#endDate1").hide();
	        $("#startDate").val(null);
	        $("#startDate").datepicker( "destroy" );
	        $("#startDate").datepicker({
	            dateFormat: 'dd/mm/yy',
	
	        });
	        date_flag = "0";
	        $("#endDate").val(null);
	        $("#endDate").datepicker( "destroy" );
	        $("#endDate").datepicker({
	            dateFormat: 'dd/mm/yy',
	
	        });        
	    });
	
	    $("#startDate").change(function(){
	        if(date_flag == "0"){
	            var from = $("#startDate").val().split("/");
	            var date = new Date(from[2], from[1] - 1, from[0]);
	            $("#endDate").datepicker( "destroy" );
	            $("#endDate").datepicker({
	                dateFormat: 'dd/mm/yy',
	                minDate: date,
	
	            });
	        }
	    });
	
	
	    var xyz;
	    function delete_user_detail(id) {
	        xyz = id;
	        $("#delete_user").modal('show');
	   }
	
	function inactive_user() {
	    $("#delete_user").modal('hide');
	        var  user_id = xyz;
	        $.ajax({
	            type: 'POST',
	            url: '/delete-subscriber/',
	            data: {'user_id': user_id},
	            success: function (response) {
							  if (response.success == 'Expired') {		
						  			location.href = '/backoffice/?status=Expired'
						  		}                
	            console.log(response);
	                if (response.success == 'true') {
	                    $("#delete_user").modal('hide');
	                  $("#remove_user").modal('show');
	                  
	                }
	                if (response.success == 'false') {
	                    alert(response.message);
	                }
	            },
	                            beforeSend: function () {
	            $("#processing").css('display','block');
	            },
	            complete: function () {
	                $("#processing").css('display','none');
	            },
	            error: function (response) {
	            console.log(response);
	                alert('error');
	            },
	        });    
	    }
	
	    var tuv;
	    function delete_users_detail(id) {
	        tuv = id;
	        $("#delete_users").modal('show');
	    }
	    function inactive_users() {
	        $("#delete_users").modal('hide');
	        var  user_id = tuv;
	        $.ajax({
	            type: 'POST',
	            url: '/delete-subscriber/',
	            data: {'user_id': user_id},
	            success: function (response) {
							  if (response.success == 'Expired') {		
						  			location.href = '/backoffice/?status=Expired'
						  		}             
	            console.log(response);
	                if (response.success == 'true') {
	                    $("#delete_user").modal('hide');
	                  $("#remove_user").modal('show');
	
	                }
	                if (response.success == 'false') {
	                    alert(response.message);
	                }
	            },
	                            beforeSend: function () {
	            $("#processing").css('display','block');
	            },
	            complete: function () {
	                $("#processing").css('display','none');
	            },
	            error: function (response) {
	            console.log(response);
	                alert('error');
	            },
	        });
	    }
	
	 var var2;
	function active_subscriber(id){
	  var1 = id;
	  $("#active_premium_service").modal('show');
	    }
	    
	function activate_subscriber() {
	        var subscriber_id = var1;
	        $("#active_premium_service").modal('hide');
	        $.ajax({
	            type: 'POST',
	            url: '/active-subscriber/',
	            data: {'subscriber_id': subscriber_id},
	            success: function (response) {
							  if (response.success == 'Expired') {		
						  			location.href = '/backoffice/?status=Expired'
						  		}             
	            console.log(response);
	                if (response.success == 'true') {
	                    $("#active_premium_service").modal('hide');
	                  $("#activate_premium_service").modal('show');
	               
	                }
	                if (response.success == 'false') {
	                    
	                }
	            },
	                beforeSend: function () {
	            $("#processing").css('display','block');
	            },
	            complete: function () {
	                $("#processing").css('display','none');
	            },
	            error: function (response) {
	            console.log(response);
	               
	            },
	        });    
	    }
	    
	function textSrch(){
	    search_keyword = $("#txtSearch").val();
	    //if(search_keyword.length > 3){
	        call_href = window.location.href
	        var lastChar = call_href.substr(call_href.length - 1);
	        if(lastChar == '/'){
	            call_href = call_href+"?search_keyword="+search_keyword
	        }else{
	            call_href = call_href+"&search_keyword="+search_keyword
	        }
	        window.location=call_href
	    //}
	}
	
	function refresh_data(){
	
	$("#city_id").parent().children('.error').css("display", "none");
	$("#endDate").parent().children('.error').css("display", "none");
	$("#startDate").parent().children('.error').css("display", "none");
	$('#startDate').val("");
	$('#endDate').val("");
	$('#startDate1').val("");
	$('#endDate1').val("");
	
	
			            $('.radio').addClass("focus");
	        $('.radio').children("span").removeClass("checked");
	        $('.radio').children("span").find("input").prop('checked', false);
	        	$("#startDate").hide();
	    	$("#endDate").hide();
	    	        	$("#startDate1").show();
	    	$("#endDate1").show();
	    	$("#city_id").select2("val", "");
	    	
	    	
	          $('#date_range').css({
		'background-color': '#FFF',
	   'border-color': '#32C5D2;',
	   'color': '#32C5D2;',
	   ' background': 'transparent none repeat scroll 0px 0px;'
	    }); 	
	   $('#Six_month').css({
		'background-color': '#FFF',
	   'border-color': '#32C5D2;',
	   'color': '#32C5D2;',
	   ' background': 'transparent none repeat scroll 0px 0px;'
	    });
	
	    $('#Three_month').css({
		'background-color': '#FFF',
	   'border-color': '#32C5D2;',
	   'color': '#32C5D2;',
	   ' background': 'transparent none repeat scroll 0px 0px;'
	    });
	        $('#One_month').css({
		'background-color': '#FFF',
	   'border-color': '#32C5D2;',
	   'color': '#32C5D2;',
	   ' background': 'transparent none repeat scroll 0px 0px;'
	    });
	        $('#One_week').css({
		'background-color': '#FFF',
	   'border-color': '#32C5D2;',
	   'color': '#32C5D2;',
	   ' background': 'transparent none repeat scroll 0px 0px;'
	    });
	
	    
	}
