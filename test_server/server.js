/*
 * A simple local node server
 *
*/

var http = require('http')
 , server = http.createServer(sourcehandler);
 
server.listen(8080);
  
function sourcehandler (req, res) {
 
    console.log('request!');

   if (req.method !== "POST") {
       console.log(JSON.stringify({msg: "Bad Request Method: " + req.method, code: 406}));
       req.destroy();
   }
  
   req.once('error', function (e) {
       console.log(JSON.stringify(({err:e, msg: "Request Stream Error", code: 500})));
   });
 
   req.once('close', function (haderror) {
       console.log("REQUEST CLOSING");
   });
 
   req.setEncoding('utf8');
 
   req.pipe(process.stdout);

   /*
   console.log("Closing");
   res.writeHead(400);
   res.end("Some error.");
   req.destroy();
    */


   // Keep connection open for 30s, close with a 408
   setTimeout(function(){
      console.log("\nclosing");
     res.writeHead(408);
     res.end("timeout on active data");
     req.destroy();
   }, 30000);

   /*
   // After 50s, close with a timeout
   setTimeout(function(){
    console.log('TIMEOUT!');
    res.writeHead(522);
    res.end();
   }, 50000);
   */

}