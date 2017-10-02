function onLogin(form){
    console.log("on login " );
    username= form.username.value
    ws = new WebSocket("ws://127.0.0.1:5678/");
    
    ws.onopen= function(event){
    	console.log("Opening connection " ) ;
    	
    	data={"login" : username} ;
    	ws.send(JSON.stringify(data)	);
    }
   
   	ws.onclose = function(event){
   		console.log("Closing connection") ;
   	} 
    ws.onmessage = function (event) {
    		console.log("new message")
    		var messages = document.getElementById("msgList");
    		var message = document.createElement('li');
    		content = document.createTextNode(event.data);
    		message.appendChild(content);
    		messages.appendChild(message);
        };
    ws.onerror = function(event){
    	console.log('error')
    }
    
    document.getElementById("sendDiv").style.visibility="visible";
    document.getElementById("messageDiv").style.visibility="visible";
        
        
}


function onSend(form){
    data={"from" : username, "to" : form.to.value, "msg": form.message.value} ;
    ws.send(JSON.stringify(data));
}