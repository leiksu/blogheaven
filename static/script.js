$(document).ready(function() {
$('form#post_form').validate({
		rules: {        
			'title': "required"
		},
		
		messages: {
			'title': "Blog title is required."			
		}
	});
	

		
var original_height="1.25em"
var hover_height = "3em"
$(".entry_text").hover(
    function () {
        $(this).animate({
			height: hover_height
		});
    },
	
	function () {
        $(this).animate({
			height: original_height
		});
    }
);



$('#edit_tags_btn').live('click', function(){
		
		var entry_id = $(this).attr("name");
		$(".tag_area_"+entry_id).css("display","none");
		//alert(entry_id);
		
		tag_edit_area_css = {
		'position':"relative",			 
		'height':"80px",
		'width':"420px",
		'border':"#dadada solid",
		"display":"block"
		}
		
		cancel_button_text_css = {
		 
		'position':"relative",			
		'top':"-54px",
		'right': '-350px',		
		'height':"20px",
		'width':"50px",
		'border':"#dadada solid",
		'background':"#f0f0f0",
		'border-radius':"50px",
		'-moz-border-radius':"50px",
		'cursor': "pointer"		
		}
		$(".tag_edit_area_"+entry_id).css(tag_edit_area_css);
		
		$(".tag_edit_area_"+entry_id).find(".cancel_button_text_"+entry_id).html("Cancel");
		
		$(".cancel_button_text_"+entry_id).css(cancel_button_text_css);
		  
		 
		$("#update_tags_form_"+entry_id).css("display","block");
		
		$("#update_tags_text_area_"+entry_id).css("display","block");
		
		$("#update_tags_btn_"+entry_id).css("display","block");
		
		//alert(entry_id);
	});
	
$('#cancel_tags_btn').live('click', function(){
		//alert('canceltagbtn');
		var entry_id = $(this).attr("name");
		$(".tag_edit_area_"+entry_id).css("display","none");
		
		$(".tag_area_"+entry_id).css("display","block");
		//alert(entry_id);
		});
		
$("#dialog-confirm").dialog({
      modal: true,
            bgiframe: true,
            width: 200,
            height: 150,			
      autoOpen: false
      });


    $("#delete_entry").live('click', function(e){
        e.preventDefault();
        
	var entry_id = $(this).attr("name");
    var targetUrl = $(this).attr("href");

	// alert(entry_id);
	// alert(targetUrl);

        $("#dialog-confirm").dialog('option', 'buttons', {
                "Confirm" : function() {
                    window.location.href =  targetUrl;
                    },
                "Cancel" : function() {
                    $(this).dialog("close");
                    }
                });

        $("#dialog-confirm").dialog("open");

    });
		

});

 
  