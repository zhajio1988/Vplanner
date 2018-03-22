$(document).ready(function() {
	

	$('#likes').click(function(){
	        var catid;
	        catid = $(this).attr("data-catid");
	         $.get('/planner/like_project/', {project_id: catid}, function(data){
	                   $('#like_count').html(data);
	                   $('#likes').hide();
	               });
	    });


    	$('#suggestion').keyup(function(){
		var query;
		query = $(this).val();
		$.get('/planner/suggest_category/', {suggestion: query}, function(data){
                 $('#cats').html(data);
		});
	});

    
	$('.planner-add').click(function(){
	    var catid = $(this).attr("data-catid");
        var url = $(this).attr("data-url");
        var title = $(this).attr("data-title");
        var me = $(this)
	    $.get('/planner/auto_add_page/', {category_id: catid, url: url, title: title}, function(data){
	                   $('#pages').html(data);
	                   me.hide();
	               });
	    });

});
