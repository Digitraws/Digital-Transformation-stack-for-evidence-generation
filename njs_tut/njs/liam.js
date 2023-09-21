var res = "";
var buf = 0;

function get_body(r, data, flags) {
	// ngx.log(1, "came here ==========================");
	if (data.length) buf++;
	res += data; // Collect the entire response,
	if (flags.last) {
		//  until we get the last byte.
		try {
			r.headersOut["syze"] = res.length;
			r.sendBuffer(res, flags);
			ngx.log(1, `FILTERED ${res.length} bytes in ${buf} buffers`);
		} catch (e) {
			ngx.log(ngx.ERR, `ERROR ${e}`);
			r.sendBuffer("", flags);
		}
	}
}

function set_header(r) {
	r.headersOut["X-My-Header"] = res.length;
}

async function get_content(r) {
	// yehi nahi aa rha
	// let res = await r.subrequest("/proxy" + r.uri, r.args);

	// const fetch = require("node-fetch");
	let url = "http://" + r.headersIn["Host"] + "/proxy" + r.uri;
	ngx.log(1, url);
	// let res = await ngx.fetch(url);
  let reply = await ngx.fetch('http://nginx.org');


	// ngx.log(1, "Subrequest success: " + res.status);
	if (res.status === 200) {
		// 	r.status = 200;
		// for (const key in res.headers) {
		// 	if (res.headers.hasOwnProperty(key)) {
		// 		const value = res.headers[key];
		// 		r.headersOut[key] = res.headers[key];
		// 		ngx.log(1, `Key: ${key}, Value: ${value}`);
		// 	}
		// }

		// r.sendHeader();
		// r.send(res.responseBuffer);
		// ngx.log(1, res.responseBuffer.size);
		// let chunk;
		// while ((chunk = await res.read())) {
		// 	ngx.log(1, chunk.length);
		// 	r.send(chunk);
		// }
		r.send("1");
		// r.finish();
		// r.headersOut = res.headersOut;
		// r.return(res.status, res.responseBuffer);
	} else {
		ngx.log(1, "Subrequest failed: " + res.status);
		r.return(res.status, res.responseBuffer);
	}
}

export default { get_body, set_header, get_content };
