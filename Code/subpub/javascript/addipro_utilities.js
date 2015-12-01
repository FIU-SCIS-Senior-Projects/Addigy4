function connect_to(protocol, port){
    connected_using = protocol;
    using_port = port;
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
                computer_information(protocol, port, "false"), 'DemoTest');
    $("#connect-ssh-button").attr("disabled", "disabled");
    $("#connect-vnc-button").attr("disabled", "disabled");
    $("#connect-web-button").attr("disabled", "disabled");
    $("#connect-ssh-button").hide();
    $("#connect-vnc-button").hide();
    $("#connect-web-button").hide();
    $("#disconnect").removeAttr("disabled");
    $("#disconnect").show();
 }

function disconnect() {
  PUBSUB.send('/exchange/testcorp.messages/test1', {"content-type":"text/plain"},
              computer_information(connected_using, using_port, "true"), 'DemoTest');
    $("#disconnect").hide();
    $("#disconnect").attr("disabled", "disabled");
    $("#connect-ssh-button").show();
    $("#connect-vnc-button").show();
    $("#connect-web-button").show();
    $("#connect-ssh-button").attr("disabled", "disabled");
    $("#connect-vnc-button").attr("disabled", "disabled");
    $("#connect-web-button").attr("disabled", "disabled");
    document.getElementById("mach1").value = "";
    document.getElementById("mach2").value = "";
    document.getElementById("connect-to-display").innerHTML = "Not Connected";
    document.getElementById("connect-from-display").innerHTML = "Not Connected";


}

function print_to_div(message) {
    document.getElementById("login-history").innerHTML += "<a>" + message + "</a></br>";
}

function set_connect_to(computer_name, id){
    computer_to = id;
    document.getElementById("mach1").value = computer_name;
    document.getElementById("connect-to-display").innerHTML = document.getElementById("mach1").value;
    $('input:first').trigger('change');
}

function set_connect_from(computer_name, id){
    computer_from = id;
    document.getElementById("mach2").value = computer_name;
    document.getElementById("connect-from-display").innerHTML = document.getElementById("mach2").value;
    $('input:first').trigger('change');
}

function computer_information(protocol, port, disconnect_flag) {
    var message_to_client = {};
    var client_info = {};
    var pubsubId;
    client_info["disconnect"] = disconnect_flag;
    client_info["tunnel_port"] = port;
    client_info["connection_type"] = protocol;
    client_info["local_port"] = "3000";
    client_info["tunnel_id"] = "fc86c7ef-f579-4115-8137-289b8a257803";
    client_info["target"] = "client";

    message_to_client[computer_from] = client_info;

    var tunnel_info = {};
    tunnel_info["target"] = "tunneler";
    tunnel_info["disconnect"] = disconnect_flag;
    tunnel_info["tunnel_id"] = "fc86c7ef-f579-4115-8137-289b8a257803";
    tunnel_info["messageToClient"] = message_to_client;
    var tunnelJson = {};
    tunnelJson[computer_to] = tunnel_info;
    tunnelJson["disconnect"] = "false";
    var information = JSON.stringify(tunnelJson);
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
    $("#disconnect").hide();
    $("#disconnect").attr("disabled", "disabled");
    $("#connect-ssh-button").attr("disabled", "disabled");
    $("#connect-vnc-button").attr("disabled", "disabled");
    $("#connect-web-button").attr("disabled", "disabled");
    $('input[type=hidden]').change(function(){
            var validated = false;
            if($('#mach1').val() != '' && $('#mach2').val() != '') {
                validated = true;
            }
            //If form is validated enable form
            if(validated) {
                $("#connect-ssh-button").removeAttr("disabled");
                $("#connect-vnc-button").removeAttr("disabled");
                $("#connect-web-button").removeAttr("disabled");
            }
      });
 });
