function initializePubSub(){

}

function connect_to_ssh(){
   var connect_from_drop_down = document.getElementById("connect_from");
   var computer_to_connect_to = connect_from_drop_down.options[connect_from_drop_down.selectedIndex].text;
   print_to_div("Now connecting to "+computer_to_connect_to);
   PUBSUB.send('/exchange/testcorp.messages', {"content-type":"text/plain"}, computer_information(computer_to_connect_to, 'ssh'), 'DemoTest');

   PUBSUB.subscribe("/queue/DemoTest", function(d) {
     print_to_div(d.body);
   }, "DemoTest");
 }

function print_to_div(message) {
   console.log(message);
}

function computer_information(computer, p) {
  var information = JSON.stringify({
"1c86c7ef-f579-4115-8137-289b8a257803": {
"target": "client",
"tunnel_id": "fc86c7ef-f579-4115-8137-289b8a257803",
"local_port": "3000",
"connection_type": "ssh"
},
"0c86c7ef-f579-4115-8137-289b8a257803": {
"target": "tunneler",
"tunnel_id": "zc86c7ef-f579-4115-8137-289b8a257803"
}
} );
  print_to_div(information);
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
 });
