var res_length = 0;
var buf = 0;
var res = "";
var timestamp = null;
var sign;
const pemEncodedKey = `-----BEGIN PRIVATE KEY-----
MIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEAwj2g1tfeH8DadiDf\
562BsjRDb7nTtaoSYZGMKdsZAb0Vlm6mNksvl6r1WsD6BmTFBglcM82e9XBBGNlB\
+8Y5SwIDAQABAkBU0CQSq19J7iN1wRUDTDd9YGSxvCo9AG3WPH8/J3Pb1bhavsa/\
CwvVSSI+9qmDYqiyJWX8akF7tWqMPi5mlJGBAiEA+KWgj3b7Fz44+IDA1QAMkjOZ\
zYChUw5CUDekNdJYKsMCIQDH/B7gTaVzT09H/1njF44f4o5CUfsl2M3XGasKQip+\
2QIfXy8IR+NEO6GWLYscRm2+Yjlep0yWdTUALbUfJ3teRQIhAMcYBDEwe//BPF+k\
IvvHbpHlvdTewxaZsctsXXB4ENB5AiEA3iVxufj4okBsDjRud+Z0B0nXmqf+uswX\
2aOA2d+kekk=\
-----END PRIVATE KEY-----`;

async function importPrivateKey(pem) {
	const pemHeader = "-----BEGIN PRIVATE KEY-----\n";
	const pemFooter = "\n-----END PRIVATE KEY-----";
	var pemContents = pem.substring(
		pemHeader.length,
		pem.length - pemFooter.length
	);
	const binaryDer = Buffer.from(pemContents, "base64");
	const key = await crypto.subtle.importKey(
		"pkcs8",
		binaryDer,
		{ name: "RSA-PSS", hash: "SHA-256" },
		false,
		["sign"]
	);
	return key;
}

async function set_sign(r, data, flags) {
	ngx.log(1, "X-Signature");
	ngx.log(1, r.headersOut["X-Signature-timestamp"]);

	if (timestamp === null) {
		timestamp = r.headersOut["X-Signature-timestamp"];
	}

	if (data.length) {
		buf++;
		res_length += data.length;
		res += data;
	}

	if (flags.last) {
		try {
			let privateKey = await importPrivateKey(pemEncodedKey);
			let buff = Buffer.from(timestamp + res);
			sign = await crypto.subtle.sign(
				{
					name: "RSA-PSS",
					hash: "SHA-256",
					saltLength: 0,
				},
				privateKey,
				buff
			);

			sign = Buffer.from(sign).toString("hex");
			ngx.log(1, sign);
			ngx.log(1, `FILTERED ${res_length} bytes in ${buf} buffers inside`);
		} catch (e) {
			ngx.log(ngx.ERR, `ERROR ${e}`);
			r.sendBuffer("", flags);
		}
	}
	// ngx.log(1, `FILTERED ${res_length} bytes in ${buf} buffers`);
	r.sendBuffer(data, flags);
}

function get_sign() {
	return sign;
}

export default { set_sign, get_sign };

/**
 * TODO
 * 1. sign using the private key of SSL certificate
 * 2. can calculate the hash smartly instead of storing the entire response
 * 3. generate timestamp on the fly
 */
