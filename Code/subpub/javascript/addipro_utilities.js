function initialize_pubsub()
{
   this.PUBSUB = new PubSub({
          location: 'http://addigy-dev.cis.fiu.edu:15674/stomp',
          login: 'test1',
          password: 'test1',
          heartbeats_outcoming: 10000,
          heartbeats_incoming: 10000
  });

  this.PUBSUB.connect('/');
}

function connect_to_shh(){
   var connect_from_drop_down = document.getElementById("connect_from");
   var computer_to_connect_to =
   connect_from_drop_down.options[connect_from_drop_down.selectedIndex].text;

   print_to_div("Now connecting to "+computer_to_connect_to);

   this.PUBSUB.send('/queue/DemoTest', {"content-type":"text/plain"}, computer_information(computer_to_connect_to, 'ssh'));
}

function print_to_div(message) {
   document.getElementById('connecting_from_output').innerHTML += '<br>' + message;
}

function computer_information(computer, p) {
  var information = "{ computer_id:" + computer+ ", protocol:"+ p + " }";
  print_to_div(information);
  return information;
}

function on_connect() {
     this.PUBSUB.subscribe('/queue/DemoTest', function(d){
       print_to_div(d.body);
     });
}
