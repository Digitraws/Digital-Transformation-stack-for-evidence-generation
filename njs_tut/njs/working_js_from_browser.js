var res_length = 0;
var buf = 0;
var res = "";
var sign;
const pemEncodedKey = `-----BEGIN PRIVATE KEY-----
MIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEAwj2g1tfeH8DadiDf
562BsjRDb7nTtaoSYZGMKdsZAb0Vlm6mNksvl6r1WsD6BmTFBglcM82e9XBBGNlB
+8Y5SwIDAQABAkBU0CQSq19J7iN1wRUDTDd9YGSxvCo9AG3WPH8/J3Pb1bhavsa/
CwvVSSI+9qmDYqiyJWX8akF7tWqMPi5mlJGBAiEA+KWgj3b7Fz44+IDA1QAMkjOZ
zYChUw5CUDekNdJYKsMCIQDH/B7gTaVzT09H/1njF44f4o5CUfsl2M3XGasKQip+
2QIfXy8IR+NEO6GWLYscRm2+Yjlep0yWdTUALbUfJ3teRQIhAMcYBDEwe//BPF+k
IvvHbpHlvdTewxaZsctsXXB4ENB5AiEA3iVxufj4okBsDjRud+Z0B0nXmqf+uswX
2aOA2d+kekk=
-----END PRIVATE KEY-----`;

function base64ToArrayBuffer(base64) {
	var binaryString = atob(base64);
	var bytes = new Uint8Array(binaryString.length);
	for (var i = 0; i < binaryString.length; i++) {
		bytes[i] = binaryString.charCodeAt(i);
	}
	return bytes.buffer;
}

async function importPrivateKey(pem) {
	// fetch the part of the PEM string between header and footer
	const pemHeader = "-----BEGIN PRIVATE KEY-----\n";
	const pemFooter = "\n-----END PRIVATE KEY-----";
	var pemContents = pem.substring(
		pemHeader.length,
		pem.length - pemFooter.length
	);
	console.log(pemContents.length, pemContents);
	const binaryDer = base64ToArrayBuffer(pemContents);

	return crypto.subtle.importKey(
		"pkcs8",
		binaryDer,
		{
			name: "RSA-PSS",
			hash: "SHA-256",
		},
		true,
		["sign"]
	);
}

async function set_sign(data) {
	let privateKey = await importPrivateKey(pemEncodedKey);
	sign = await crypto.subtle.sign(
		{
			name: "RSA-PSS",
			hash: "SHA-256",
			saltLength: 0,
		},
		privateKey,
		data
	);
	sign = [...new Uint8Array(sign)]
		.map((b) => b.toString(16).padStart(2, "0"))
		.join("");
}

function get_sign() {
	return sign;
}

/* RUN on Console*/
var enc = new TextEncoder(); // always utf-8
var buff = enc.encode("Hello World");
console.log(buff);
set_sign(buff).then(() => {
	var sgn = get_sign();
	console.log(sgn);
});