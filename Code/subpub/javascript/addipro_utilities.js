function connect_to_ssh(){
    PUBSUB.subscribe("/exchange/testcorp.presence/" + "", function(d) {
				    if(d.headers.action == "bind"){        
                        print_to_div(d.headers.key + " has logged on");
                    }              
                    else if(d.headers.action == "unbind") {
                        print_to_div(d.headers.key + " has logged off");
                    }
				 });
    PUBSUB.subscribe("/exchange/testcorp.presence/test1", function(d) {
                    if(d.headers.action == "bind"){        
                        console.log();
                    }
				 });
    PUBSUB.subscribe("/exchange/testcorp.messages", function(d) {
            console.log();
        }, "DemoTest");
    PUBSUB.send('/exchange/testcorp.messages/test1', {"content-type":"text/plain"}, 
                computer_information(computer_to, 'ssh'), 'DemoTest');
 }

function print_to_div(message) {
    document.getElementById("login-history").innerHTML += "<a>" + message + "</a></br>";
}

function set_connect_to(){
    computer_to = "0c86c7ef-f579-4115-8137-289b8a257803";
    document.getElementById("mach1").value = computer_to;
    document.getElementById("connect-to-display").innerHTML = document.getElementById("connect-to-1").innerHTML;
    $('input:first').trigger('change');
}
    
function set_connect_from(){
    computer_from = "0c86c7ef-f579-4115-8137-289b8a257803";
    document.getElementById("mach2").value = computer_from;
    document.getElementById("connect-from-display").innerHTML = document.getElementById("connect-from-1").innerHTML;
    $('input:first').trigger('change');
}

function computer_information(computer, p) {
    var information = JSON.stringify({ 
        "0c86c7ef-f579-4115-8137-289b8a257803": { 
            "target": "tunneler", 
            "tunnel_id": "fc86c7ef-f579-4115-8137-289b8a257803", 
            "messageToClient": { 
                "0c86c7ef-f579-4115-8137-289b8a257803": { 
                    "target": "client", 
                    "tunnel_id": "fc86c7ef-f579-4115-8137-289b8a257803", 
                    "local_port": "3000", 
                    "connection_type": "ssh" 
                } 
            } 
        } 
      });
    return information;
}

$(document).ready(function() {
    PUBSUB = new PubSub({
            location: 'http://addigy-dev.cis.fiu.edu:15674/stomp',
            login: 'test1',
            password: 'test1',
            heartbeats_outcoming: 0,
            heartbeats_incoming: 0,
            organization: 'testcorp'
    });
    
    
    PUBSUB.connect('/');
    $("#connect-ssh-button").attr("disabled", "disabled");
    $('input[type=hidden]').change(function(){
            var validated = false;
            if($('#mach1').val() != '' && $('#mach2').val() != '') {
                validated = true;
            }
            //If form is validated enable form
            if(validated) {
                $("#connect-ssh-button").removeAttr("disabled");   
            }
      });
 });
