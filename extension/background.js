chrome.runtime.onMessage.addListener(async function (
	request,
	sender,
	sendResponse
) {
	console.log("background.js received message");
	console.log(request);
	let res = await chrome.runtime.sendNativeMessage(
		"digitraws",
		JSON.stringify(request)
	);
	console.log(res);
	// await sendResponse(res);
	return res;
});
