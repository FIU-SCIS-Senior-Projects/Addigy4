user = "";
function HDD_check(protocol, port){
    print_to_div("+================================+");
    print_to_div("CHECKING ALL HARD DRIVES...");
    PUBSUB.publish('/exchange/examplesoft.messages/lazy admin', {"content-type":"text/plain"}, "HDD_roll_call", 'lazy admin');
 }

function connect() { 
    PUBSUB.subscribe("/exchange/examplesoft.presence/" + "", function(d) {
                    employee = d.headers['key'];
				 });
    PUBSUB.subscribe("/exchange/examplesoft.presence/lazy admin", function(d) {
                    if(d.headers.action == "bind"){
                        console.log();
                    }
				 });
    PUBSUB.subscribe("/exchange/examplesoft.messages", function(d) {
        if(d.exchange == "examplesoft.messages" && d.body != "HDD_roll_call") {
            print_to_div(employee + " HARD DRIVE STATUS: " + d.body);
        }
    }, "lazy admin");  
    $("#connect").attr("disabled", "disabled");
    $("#connect").hide();
    $("#CheckHardDrives").removeAttr("disabled");
    $("#CheckHardDrives").show();
}

function print_to_div(message) {
    document.getElementById("login-history").innerHTML += "<a>" + message + "</a></br>";
}

$(document).ready(function() {
    PUBSUB = new PubSub({
            addr: 'http://localhost:15674/stomp',
            username: 'lazy admin',
            password: 'lazy',
            heartbeats_outcoming: 0,
            heartbeats_incoming: 0,
            organization: 'examplesoft'
    });

    $("#CheckHardDrives").attr("disabled", "disabled");
    $("#CheckHardDrives").hide();
    PUBSUB.connect('/');
 });
