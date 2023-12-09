document.getElementById("runCommand").addEventListener("click", () => {
	document.getElementById("runCommand").disabled = true;
	document.getElementById("loader").style.display = "block";
	document.getElementById("result").innerText = "";

	let url = document.getElementById("url").value;
	let filepath = document.getElementById("filepath").value;

	chrome.runtime.sendMessage({ url, filepath }, function (response) {
		console.log(response);
		document.getElementById("runCommand").disabled = false;
		document.getElementById("loader").style.display = "none";
		document.getElementById("result").innerText = response;
	});
});
