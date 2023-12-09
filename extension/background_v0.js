chrome.runtime.onMessage.addListener(async function (
	request,
	sender,
	sendResponse
) {
	console.log("background.js received message");
	console.log(request);
	const url = request.url;
	const filename = request.filename;
	let res = await chrome.downloads.download({ url: url, filename: filename });
	await sendResponse({ result: res });
	return true;
});

function onResponse(response) {
	console.log(`Received ${response}`);
}

function onError(error) {
	console.log(`Error: ${error}`);
}

chrome.action.onClicked.addListener(() => {
	console.log("Sending:  ping");
	let sending = browser.runtime.sendNativeMessage("ping_pong", "ping");
	sending.then(onResponse, onError);
});
