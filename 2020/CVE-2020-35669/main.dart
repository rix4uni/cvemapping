import 'package:http/http.dart';
import 'package:http/src/request.dart';

void main() async {
  var r = Request(
      "GET http://example.com/ HTTP/1.1\r\nHost: example.com\r\nLLAMA:",
      Uri(scheme: "http", path: "/llama", host: "google.com"));
  var rs = await r.send();
  var resp = await Response.fromStream(rs);
  print('${resp.body}');
  print('${resp.headers}');
}
