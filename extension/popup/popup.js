(function () {
	var captureButton = document.getElementById("whatToCapture");

	captureButton.onclick = function (event) {
		// check if devtools is open
		chrome.extension.sendMessage(
			{ action: "getDevToolsStatus" },
			function (response) {
				if (!response.data) {
					alert("DevTools needs to be open to get HAR logs");
				} else {
					// sends message to devtools(through background.js)
					let message = { action: "downloadHARlog" };
					chrome.extension.sendMessage(message, function (a) {
						// alert(JSON.stringify(a));
					});
				}
			}
		);
	};
})();