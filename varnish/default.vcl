vcl 4.0;

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
    if (beresp.ttl <= 0s ||
        beresp.http.Set-Cookie ||
        beresp.http.Surrogate-control ~ "no-store" ||
        (!beresp.http.Surrogate-Control &&
        beresp.http.Cache-Control ~ "no-cache|no-store|private") ||
        beresp.http.Vary == "*") {

        set beresp.ttl = 120s;
        set beresp.uncacheable = true;
    }
  set beresp.ttl = 5m;
}