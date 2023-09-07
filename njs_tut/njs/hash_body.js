function addCustomHash(response) {
	var crypto = require("crypto");
	var hash = crypto.createHash("sha256");
	hash.update(response.body);
	var customHash = hash.digest("hex");
	response.headersOut["Custom-Hash"] = customHash;
	return response;
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
