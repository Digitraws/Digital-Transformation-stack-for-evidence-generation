var hash = "";
var res = "";
var buf = 0;

function set_hash(r, data, flags) {
	if (data.length) buf++;
	res += data; // Collect the entire response,
	if (flags.last) {
		//  until we get the last byte.
		try {
			hash = require("crypto").createHash("sha1").update(res).digest("base64");
			r.sendBuffer(res, flags);
			ngx.log(ngx.INFO, `FILTERED ${res.length} bytes in ${buf} buffers`);
		} catch (e) {
			ngx.log(ngx.ERR, `ERROR ${e}`);
			r.sendBuffer("", flags);
		}
	}
}

function get_hash() {
	return hash;
}

export default { set_hash, get_hash };

/**
 * TODO
 * 1. create functionality for signature
 * 2. can calculate the hash smartly instead of storing the entire response
 * 3. sign using the private key of SSL certificate
 */
