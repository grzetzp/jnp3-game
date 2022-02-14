vcl 4.0;

import directors;

backend server1 {
  .host = "app";
  .port = "5000";
  .probe = {
    .url = "/";
    .timeout = 1s;
    .interval = 3s;
    .window = 5;
    .threshold = 3;
  }
}

backend server2 {
  .host = "appreplica";
  .port = "5000";
  .probe = {
    .url = "/";
    .timeout = 1s;
    .interval = 3s;
    .window = 5;
    .threshold = 3;
  }
}



sub vcl_init {
    new balancer = directors.round_robin();
    balancer.add_backend(server1);
    balancer.add_backend(server2);
}

sub vcl_recv {
    set req.backend_hint = balancer.backend();
}

sub vcl_backend_response {
  set beresp.ttl = 5m;
}