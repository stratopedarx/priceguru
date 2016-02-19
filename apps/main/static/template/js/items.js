$(document).ready(function(){
	var userItemPopUp = new Popup('#useritem-popup', '#fade');
	
	
	$('#add-useritem-btn').on('click', function(){
		userItemPopUp.open();
		return false;
	});
	
	
	$('#close-useritem').on('click', function(){
		userItemPopUp.close();
		return false;
	});
	
	var listUserItemPopUp = new Popup('#list-useritem-popup', '#fade');
	
	$('#edit-useritem-btn').on('click', function(){
		listUserItemPopUp.open();
		$('#useritems-list-action').val('edit');
		$('.list-action-text').html('edit');
		var checked_items = $('.checked_items:checked');
		var html = '';
		for(var i = 0; i < checked_items.length; i++){
			html = '';
			html += '<tr>';
			html += '<td><input type="text" class="form-control edit-item" pid="'+$($('.checked_items:checked')[i]).val()+'" value="'+ $($('.checked_items:checked')[i]).parent().parent().children()[1].innerHTML + '" /></td>';
			html += '</tr>';
			$('#list-to').append(html);
		}
		
		return false;
	});
	
	
	
	$('#delete-useritem-btn').on('click', function(){
		listUserItemPopUp.open();
		$('#useritems-list-action').val('delete');
		$('.list-action-text').html('delete');
		var checked_items = $('.checked_items:checked');
		var html = '';
		for(var i = 0; i < checked_items.length; i++){
			html = '';
			html += '<tr>';
			html += '<td>'+ $($('.checked_items:checked')[i]).parent().parent().children()[1].innerHTML + '</td>';
			html += '<td>'+ $($('.checked_items:checked')[i]).parent().parent().children()[2].innerHTML + '</td>';
			html += '</tr>';
			$('#list-to').append(html);
		}
		
		return false;
	});
	
	
	$('#close-list-useritem').on('click', function(){
		listUserItemPopUp.close();
		$('#useritems-list-action').val('');
		$('#list-to').html('');
		return false;
	});
	
	$('#no-list-useritems-btn').on('click', function(){
		$('#useritems-list-action').val('');
		listUserItemPopUp.close();
		$('#list-to').html('');
		return false;
	});
	
	function editItems(btn){
		var edit_items = $('.edit-item');
		var items = {};
		for(var i = 0; i < edit_items.length; i++){
			console.log($(edit_items[i]).attr('pid') +' - ' + $(edit_items[i]).val());
			items[$(edit_items[i]).attr('pid')] = $(edit_items[i]).val();
		}
		$.ajax({
			url: USERITEM_EDIT,
			method: 'POST',
			data: items,
			dataType: 'json',
			success: function(data){
				console.log(data);
				$('#useritems-list-action').val('');
				listUserItemPopUp.close();
				$(btn).removeAttr('disabled');
				var checked_items = $('.checked_items:checked');
				for(var i = 0; i < checked_items.length; i++){
					$($('.checked_items:checked')[i]).parent().parent().children()[1].innerHTML = items[$($('.checked_items:checked')[i]).attr('pid')];
				};
				$('#list-to').html('');
			},
			error: function(data){ 
					console.log('error'); 
					console.log(data['responseText']); 
					$(btn).removeAttr('disabled');
			}
		});
		console.log(items);
		$(btn).removeAttr('disabled');
	}
	
	function deleteItems(btn){
		var checked_items = $('.checked_items:checked');
		var items = [];
		for(var i = 0; i < checked_items.length; i++){
			items.push($($('.checked_items:checked')[i]).val());
		}
		$.ajax({
				url: USERITEM_DELETE,
				method: 'POST',
				data: {'items':items},
				success: function(data){
					console.log(data);
					for(var i = 0; i < items.length; i++){
						$('#item-'+items[i]).remove();
						$('#active-group').children()[1].innerHTML -= 1;
					}
				
					$('#list-to').html('');
					var items_left = $('.checked_items');
					
					if(items_left.length == 0){
						$($('.table-list tbody')[0]).html('<tr id="no-items-label"><td colspan="5"><h3 class="muted" align="center">Please add item</h3></td></tr>');
					}
					$('#useritems-list-action').val('');
					listUserItemPopUp.close();
					$(btn).removeAttr('disabled');
								
				},
				error: function(data){ 
					console.log('error'); 
					console.log(data['responseText']); 
					$(btn).removeAttr('disabled');
					
				}
			});
	}
	
	$('#submit-item-list').on('click', function(){
		var btn = this;
		if(!$(btn).attr('disabled')){
			$(btn).attr('disabled', 'disabled');
			
			if($('#useritems-list-action').val() == 'delete'){
				deleteItems(btn);
			}
			else if($('#useritems-list-action').val() == 'edit'){
				editItems(btn);
			}
			
			
		}
	});
	
	     var alertTimeout = 4000;

        function setAddItemFormDisabled(disabled) {
            $("#add-item-form a.btn-success").prop("disabled", disabled);
            $("#add-item-form input#id_url").prop("disabled", disabled);
        }

        function setAddItemFormMessage(message, cls) {
            var messageEl = $("#message");
            if (message != "") {
                messageEl.show();
                messageEl.html(message);
                messageEl.attr("class", "alert alert-" + cls);
            }
            else {
                messageEl.hide();
            }
        }

        function startAddItemTaskStatusUpdating(taskId) {
            var updateIntervalId = setInterval(function() {
                $.ajax({
                    url: "/api/is_ready/" + taskId,
                    success: function(res) {
                        if (res.ready) {
                            var itemUrl = $("#add-item-form #id_url").val();
							
                            if (res.data.success) {
                                setAddItemFormMessage("Item '" + itemUrl + "'' is added!", "success");
                                setAddItemFormMessage("");
								html = '';
							    html += '<tr id="item-'+res.data.result.user_item['pk']+'">';
								html += '<td><input type="checkbox" pid="'+res.data.result.user_item['pk']+'" class="checked_items" value="'+res.data.result.user_item['pk']+'" /></td>';
								html += '<td>'+res.data.result.item.fields['title']+'</td>';
								html += '<td><a href="'+res.data.result.item.fields['url']+'">'+res.data.result.item.fields['url']+'</a></td>';
								html += '<td style="vertical-align:middle">'+res.data.result.price.fields['current_price']+' '+res.data.result.price.fields['currency']+'</td>';
								html += '<td style="vertical-align:middle">'+res.data.result.price['formatted_date']+'</td>';
								html += '<td>'+res.data.result.partner.fields['name']+'</td>';
								html += '</tr>';
								$('#no-items-label').remove();
								$('.table-list tbody').append(html);
								$('#active-group').children()[1].innerHTML = parseInt($('#active-group').children()[1].innerHTML) + 1;
                                userItemPopUp.close();
								
                                
                            }
                            else {
                                var msg = null;
                                if (res.data.error.name == "IntegrityError"){
                                    msg = "Item '" + itemUrl + "' already exists!";
                                } else {
                                    msg = "Something went wrong :(";

                                }
                                console.log("Adding item has been failed with error: " + res.data.error.name);
                                setAddItemFormMessage(msg, "error");
                                setTimeout(function() {
                                    setAddItemFormMessage("");
                                }, alertTimeout);
                            }
                            setAddItemFormDisabled(false);

                            clearInterval(updateIntervalId);
							$('#add-item-submit').removeAttr('disabled');
                        }
                        console.log(res);
                    }
                })
            }, 1000);
        }

        
            setAddItemFormDisabled(false);
            setAddItemFormMessage("");

            $(document).on("click", "#add-item-submit", function() {   
				$('#add-item-submit').attr('disabled', 'disabled');			
				var form = $('#add-item-form');
                //var url = form.url.value;
                $.ajax({
                    url: form.action,
                    type: "POST",
                    data: form.serialize(),
                    success: function(taskId) {
                        startAddItemTaskStatusUpdating(taskId);
                    },
                    error: function(res) {
                        setAddItemFormMessage(res.responseText, "error");
                        setAddItemFormDisabled(false);
                        setTimeout(function() {
                            setAddItemFormMessage("");
                        }, alertTimeout);
                    },
                });

                setAddItemFormDisabled(true);
                var itemUrl = $("#add-item-form #id_url").val();
                setAddItemFormMessage("Adding item '" + itemUrl + "' is in progress...", "info");

                return false;
            });
       
	
	
});
	