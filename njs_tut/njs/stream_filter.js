// stream_filter.js

function myStreamFilter(s) {
	// Perform stream-level data manipulation here
	// Access s for stream session information
	s.on("data", function (chunk) {
		// Modify the incoming data chunk as needed
		// For example, you can log or manipulate the data
		// before it's sent to the client or upstream server.
		ngx.log(1, chunk);
		s.send(chunk);
	});
}

function getSign(r) {
	var len = r.requestText;
	ngx.log(1, "response body length: " + len);
	return len;
}

export default { getSign };
