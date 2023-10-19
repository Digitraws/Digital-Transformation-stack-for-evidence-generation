var res_length = 0;
var buf = 0;
var hash = require("crypto").createHash("sha1");

function set_hash(r, data, flags) {
	if (data.length) {
		buf++;
		res_length += data.length;
	}
	hash.update(data);

	//  until we get the last byte.
	if (flags.last) {
		try {
			hash = hash.digest("base64");
			r.sendBuffer(res, flags);
			ngx.log(ngx.INFO, `FILTERED ${res_length} bytes in ${buf} buffers`);
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
