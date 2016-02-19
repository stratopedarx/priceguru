$(document).ready(function(){
	function renderGroupLi(data){
		var text = '<li><a href="'+ITEMGROUP_URL+data['id']+'/">' + data['group_name'];
		text += '<span class="badge">0</span></a></li>';
		return text;
	}
	
	var addGroupPopUp = new Popup('#add-group-popup', '#fade');
		
	$('#add-group-btn').on('click', function(){
		addGroupPopUp.open();
		return false;
	});
	
	
	$('#close-add-group').on('click', function(){
		addGroupPopUp.close();
		return false;
	});
	

	
	$('#edit-group-btn').on('click', function(){
		addGroupPopUp.open();
		return false;
	});
	
	$('#add-group-submit').on('click', function(){
		var btn = this;
		if(!$(btn).attr('disabled')){
			$(btn).attr('disabled', 'disabled')
			$.ajax({
				url: CREATE_GROUP_URL,
				method: 'POST',
				data: {'group_name': $('#group_name').val()},
				success: function(data){
					console.log(data);
					$(btn).removeAttr('disabled');
					$('#group_name').val('');
					addGroupPopUp.close();
					$('ul.groups').append(renderGroupLi(data));
					
				},
				error: function(data){ 
					console.log('error'); 
					console.log($.parseJSON(data['responseText'])); $(btn).removeAttr('disabled');
					
				}
			})
		}
		return false;
	});
	
	
	$('#edit-group-submit').on('click', function(){
		var btn = this;
		if(!$(btn).attr('disabled')){
			$(btn).attr('disabled', 'disabled')
			$.ajax({
				url: UPDATE_GROUP_URL,
				method: 'POST',
				data: {'group_name': $('#group_name').val(), 'pk': $('#active-group').attr('gid')},
				success: function(data){
					console.log(data);
					$(btn).removeAttr('disabled');
					$('#group_name').val(data['group_name']);
					addGroupPopUp.close();
					var groupNameNodes = $('.current-groupname-text');
					var groupNameNodesLen = groupNameNodes.length; 
					for(var i = 0; i < groupNameNodesLen; i++)
					{
						console.log($(groupNameNodes[i]).html());
						$(groupNameNodes[i]).html(data['group_name']);
					}
					
				},
				error: function(data){ 
					console.log('error'); 
					console.log(data['responseText']); 
					$(btn).removeAttr('disabled');
					
				}
			});
		}
		return false;
	});
	
	
	var deleteGroupPopUp = new Popup('#delete-group-popup', '#fade');
	$('#delete-group-btn').on('click', function(){
		deleteGroupPopUp.open();
		return false;
	});
	
	$('#close-delete-group').on('click', function(){
		deleteGroupPopUp.close();
		return false;
	});
	
	$('#no-delete-group-btn').on('click', function(){
		deleteGroupPopUp.close();
		return false;
	});
	
	$('#submit-group-delete').on('click', function(){
		$(this).attr('disabled', 'disabled');
		$(this).parent().submit();
		return false;
	});
	
});