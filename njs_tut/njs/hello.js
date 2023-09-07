function hello(r) {
  ngx.log(1,"hello from njs");
  ngx.log(1,r.subrequest);
  ngx.log(1,r.rawHeadersIn);
  ngx.log(1,r.rawHeadersOut);
	r.return(200, "Hello World\n");
}

async function addCustomHash(r) {
	// var crypto = require("crypto");
	// var hash = crypto.createHash("sha256");
	// // hash.update(r.responseBuffer);
	// // hash.update(r.responseBuffer);
	// // var customHash = hash.digest("hex");
	// let propertyList = "";

	// for (let key in r) {
	// 	if (r.hasOwnProperty(key)) {
	// 		if (propertyList !== "") {
	// 			propertyList += ", ";
	// 		}
	// 		propertyList += key;
	// 	}
	// }

	// var resText = "", reqText = "";
	// if(!r.responseText) resText = "No responseText";
	// else resText = r.responseText;
	// if(!r.requestText) reqText = "No requestText";
	// else reqText = r.requestText;

	// r.headersOut["X-Custom-Hash"] = propertyList;
	// r.headersOut["X-res-text"] = resText;
	// r.headersOut["X-req-text"] = reqText;
  ngx.log("hello from njs");
  return r.return(200, "Hello World\n");
}

export default { hello, addCustomHash };
