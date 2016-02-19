var Popup = function(popup_id, fade_id){
		

		
	this.open = function(){
		if (this.is_open == false){
			$(fade_id).addClass('over');
			$(popup_id).removeClass('nodisplay');
			this.is_open = true;
		}
		
	}
	
	this.close = function(){
		if (this.is_open == true){
			$(fade_id).removeClass('over');
			$(popup_id).addClass('nodisplay');
			this.is_open = false;
		}
	}
		
	this.is_open = false;
		
}
	
/*<div id="delete-item-popup" class="popup change-photo nodisplay">
    <h4>Delete Item</h4>
    <a href="#" class="closebut" id="close-delete-item"></a>
    <div class="in">
        <h2>%ITEM%</h2>
        You are sure you want to delete this item?
        <br/><br/><br/>
        <center>
            <form>{% csrf_token %}
                <a id="submit-item-delete"  class="btn btn-default btn-lg">yes</a>&nbsp;&nbsp;<a href="#" id="no-delete-item-btn" class="btn btn-success btn-lg">no</a>
            </form>
        </center>
    </div>
</div>
*/	
var newPopup = function(popup_id, fade_id){
	
	this.close = function(){
		$(fade_id).removeClass('over');
		$(popup_id).addClass('nodisplay');
		$(popup_id).html('');
			
	}
	
	this.open = function(props){
		
		var html = '<h4>'+props['title']+'</h4>';
		html += '<a href="#" class="closebut"></a>';
		html += '<div class="in">';
		if (props['nodes'] != 'undefined'){
			for(var i = 0; i < props['nodes'].length; i++){
				var node = props['nodes'][i];
				console.log(node);
				html += '<'+node['name'];
				var attrs = Object.keys(node['attrs']);
				if(attrs.length > 0){ 
					html += ' ';
					for(var j = 0; j < attrs.length; j++){
						html += attrs[j]+'="'+node['attrs'][attrs[j]]+'" ';
					};
				}
				if (['input', 'br', 'hr'].indexOf(node['name']) == -1){
					html += '>'+node['text']+'</'+node['name']+'>';
				}
				else{
					html += '/>';
				}
			}
		}
		html += '</div>';
		$(popup_id).html(html);
		$(fade_id).addClass('over');
		$(popup_id).removeClass('nodisplay');
			
	}
	
	
}
	

	

