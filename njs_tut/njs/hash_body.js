function addCustomHash(r) {
	var crypto = require("crypto");
	var hash = crypto.createHash("sha256");
	hash.update(r.responseBody);
	var customHash = hash.digest("hex");
	r.headersOut["X-Custom-Hash"] = customHash;
	return r;
}

function doSign() {
	const {
		generateKeyPairSync,
		createSign,
		createVerify,
	} = require("node:crypto");

	const { privateKey, publicKey } = generateKeyPairSync("rsa", {
		modulusLength: 2048,
	});

	const sign = createSign("SHA256");
	sign.update("some data to sign");
	sign.end();
	const signature = sign.sign(privateKey);

	const verify = createVerify("SHA256");
	verify.update("some data to sign");
	verify.end();
	console.log(verify.verify(publicKey, signature));
	// Prints: true
}

// Export the function to be used in NGINX configuration
export default { addCustomHash };
