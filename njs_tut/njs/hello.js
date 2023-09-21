function hello(r) {
	// var res = r.responseBody;
	// ngx.log(1, res);
	r.headersOut["X-Hello"] = "val";
	// r.sendBuffer(data, flags);
}

function addCustomFooter(r) {
	// Append a custom footer to the response
	r.body += "<footer>This is a custom footer.</footer>";
	ngx.log(1, r.body);
	return r;
}

export default { hello, addCustomFooter };
