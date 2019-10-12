
function clear_dg_data() {
    $("#new_dg_name").val('');
    $("#dg_sign_attachment").val('');
}

function clear_president_data(){
    $("#new_president_name").val('');
    $("#president_sign_attachment").val('');
}

function upload_dg_info(){
var flag=true

if ($('#new_dg_name').val() == ''){
    flag=false
    $("#error_new_dg_name").addClass('has-error')
    }

if ($('#dg_sign_attachment').val() == ''){
    flag=false
    $("#error_dg_sign_attachment").addClass('has-error')
    }

    var input = document.getElementById("dg_sign_attachment");
	sign_file = input.files[0];

   var formData= new FormData();
   formData.append("sign_file",sign_file);

   formData.append("name",$("#new_dg_name").val());
   formData.append("type",1);

if (flag){
     $.ajax({
        type:'POST',
        url:'/backofficeapp/save-sign-name/',
       data: formData,
        cache: false,
        processData: false,
        contentType: false,
        success: function(response) {
            if (response.success == "true") {
                bootbox.alert("<span class='center-block text-center'>Data Stored Successfully</span>");
                clear_dg_data()
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


function upload_president_info(){
var flag=true

if ($('#new_president_name').val() == ''){
    flag=false
    $("#error_new_president_name").addClass('has-error')
    }

if ($('#president_sign_attachment').val() == ''){
    flag=false
    $("#error_president_sign_attachment").addClass('has-error')
    }

   var input = document.getElementById("president_sign_attachment");
   sign_file = input.files[0];

   var formData= new FormData();
   formData.append("sign_file",sign_file);

   formData.append("name",$("#new_president_name").val());
   formData.append("type",0);

if (flag){
    $.ajax({
        type:'POST',
        url:'/backofficeapp/save-sign-name/',
        data: formData,
        cache: false,
        processData: false,
        contentType: false,
        success: function(response) {
            if (response.success == "true") {
                bootbox.alert("<span class='center-block text-center'>Data Stored Successfully</span>");
                clear_president_data()
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

//<----for DG sign image size height width start from here  ------->
$(function() {
$("#dg_sign_attachment").change(function () {
	    if(fileExtValidate(this)) {
	    	 if(fileheightValidate(this)){
	    	     if(fileSizeValidate(this)){
	    	         if(filewidthValidate(this)){
	    	 	showImg(this);
	    	 	      }
	    	    }
	         }
	    }
    });
var validExt = ".png, .gif, .jpeg, .jpg";
function fileExtValidate(fdata) {
 var filePath = fdata.value;
 var getFileExt = filePath.substring(filePath.lastIndexOf('.') + 1).toLowerCase();
 var pos = validExt.indexOf(getFileExt);
 if(pos < 0) {
 	bootbox.alert("This file is not allowed, please upload valid file.");
 	return false;
  } else {
  	return true;
  }
}

var height = '50';
function fileheightValidate(fdata) {
	 if (fdata.files && fdata.files[0]) {
                var fheight = fdata.files[0].size/1000;
                if(fheight > height) {
                	 bootbox.alert('Maximum image height exceed, This file height is: ' + fheight + "cm");
                	 return false;
                } else {
                	return true;
                }
     }
 }

var maxSize = '20';
function fileSizeValidate(fdata) {
	 if (fdata.files && fdata.files[0]) {
                var fsize = fdata.files[0].size/1024;
                if(fsize > maxSize) {
                	 bootbox.alert('Maximum image size exceed, This file size is: ' + fsize + "KB");
                	 return false;
                } else {
                	return true;
                }
     }
 }

var width = '110';
function filewidthValidate(fdata) {
	 if (fdata.files && fdata.files[0]) {
                var fwidth = fdata.files[0].size/1000;
                if(fwidth > width) {
                	 bootbox.alert('Maximum image width exceed, This file width is: ' + fwidth + "cm");
                	 return false;
                } else {
                	return true;
                }
     }
 }

});
//<----for DG sign image size height width end from here  ------->




//<----for President sign image size height width start from here  ------->
$(function() {
$("#president_sign_attachment").change(function () {
	    if(fileExtValidate(this)) {
	    	 if(fileheightValidate(this)){
	    	     if(fileSizeValidate(this)){
	    	         if(filewidthValidate(this)){
	    	 	showImg(this);
	    	 	      }
	    	    }
	         }
	    }
    });
var validExt = ".png, .gif, .jpeg, .jpg";
function fileExtValidate(fdata) {
 var filePath = fdata.value;
 var getFileExt = filePath.substring(filePath.lastIndexOf('.') + 1).toLowerCase();
 var pos = validExt.indexOf(getFileExt);
 if(pos < 0) {
 	bootbox.alert("This file is not allowed, please upload valid file.");
 	return false;
  } else {
  	return true;
  }
}

var height = '50';
function fileheightValidate(fdata) {
	 if (fdata.files && fdata.files[0]) {
                var fheight = fdata.files[0].size/1000;
                if(fheight > height) {
                	 bootbox.alert('Maximum image height exceed, This file height is: ' + fheight + "cm");
                	 return false;
                } else {
                	return true;
                }
     }
 }

var maxSize = '50';
function fileSizeValidate(fdata) {
	 if (fdata.files && fdata.files[0]) {
                var fsize = fdata.files[0].size/1024;
                if(fsize > maxSize) {
                	 bootbox.alert('Maximum image size exceed, This file size is: ' + fsize + "KB");
                	 return false;
                } else {
                	return true;
                }
     }
 }

var width = '110';
function filewidthValidate(fdata) {
	 if (fdata.files && fdata.files[0]) {
                var fwidth = fdata.files[0].size/1000;
                if(fwidth > width) {
                	 bootbox.alert('Maximum image width exceed, This file width is: ' + fwidth + "cm");
                	 return false;
                } else {
                	return true;
                }
     }
 }

});
//<----for President sign image size height width end from here  ------->


