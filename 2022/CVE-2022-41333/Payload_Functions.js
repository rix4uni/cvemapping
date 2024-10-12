///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// CVE-2022-41333 Encryption & Decryption Functions
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// UTF8 Decode Function //
function decode_utf8(s)
{
	return decodeURIComponent(escape(s));
}
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// XOR Function //
function FV_xorString(original, magic)
{
	var out = "";
	if (original != null)
	{
		var len = original.length;
		for (var i = 0; i < len; i++)
		{
			out += String.fromCharCode((original.charCodeAt(i) ^ magic));
		}
	}
	return out;
}
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Decryption Function. //
function FV_unscramble(data, scrmableType)
{
	if (data == null)
	{
		return "";
	}
	var curpos = data.indexOf("fewRes=");
	if (curpos < 0)
	{
    alert("no data");
		return data;
	}
	var out = "";
	try
	{
		out = data.substring(0, curpos);
		curpos += 7;
		var codec = data.charAt(curpos + 1);
		var bridge_str = data.substring(7 + 3);
		if (codec == "B")
		{
			bridge_str = atob(bridge_str);
		}

		curpos = 0;
		var session_magic = 31;
		if(session_magic == 0) {
			session_magic = 31;
		}
		var header = "";
		var stop_char = "";
		if(scrmableType == null) {
			scrmableType = 0;
		}
		if(scrmableType === 2) {
			header = FV_xorString(bridge_str.substring(curpos, 1 + 1), 31);
			if (header.charAt(0) != ":")
			{
				return out;
			}
			session_magic = (header.charCodeAt(1) - "A".charCodeAt(0));
			curpos += (1 + 1);
		}
		else {
			if(scrmableType == 1) {
				session_magic = 31;
			}
			header = FV_xorString(bridge_str.substring(curpos, 1), session_magic);
			if (header.charAt(0) != ":") {
				return out;
			}
		}

		header = FV_xorString(bridge_str.substring(curpos, curpos+1), session_magic);
		if(header.charAt(0) != ":") {
			return out;
		}
		curpos += 1;
		stop_char = String.fromCharCode(session_magic ^ ":".charCodeAt(0));
		var stop_pos = bridge_str.indexOf(stop_char, curpos);
		var sizestr = FV_xorString(bridge_str.substring(curpos, stop_pos), session_magic);
		var strsize = parseInt(sizestr);
		curpos = stop_pos + 1;
		out = FV_xorString(bridge_str.substring(curpos, strsize + curpos), session_magic);
		curpos += strsize;
		out += bridge_str.substring(curpos);
		if (codec != "N")
		{
			var decodedString = decode_utf8(out);
			out = decodedString;
			prompt("Copy to clipboard: Ctrl+C, Enter", out);

		}
		return out;
	}
	catch (exp)
	{
		return out;
	}
}
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Encryption Function //
function FV_scrambler(data, codec, sessionMagic, type)
{
	if (!true)
	{
		return data;
	}

	if(type == null) {
		type = 0;
	}
	if(false) {
		type = 2;
	}

	var out = "fewReq=";
	if (!data || data.length == 0)
	{
		return out;
	}

	if (sessionMagic == 0)
	{
		sessionMagic = 31;
	}

	var ostr_magic = "" + ":" + String.fromCharCode(sessionMagic + "A".charCodeAt(0));
	var ostr_len = "" + ":" + data.length + ":";
	var ostr_scrambled = "";

	if(type == 2) {
		ostr_scrambled += FV_xorString(ostr_magic, 31);
	}
	ostr_scrambled += FV_xorString(ostr_len, sessionMagic);
	ostr_scrambled += FV_xorString(data, sessionMagic);

	out += ("" + ":" + codec + ":");
	if (codec ==  "B")
	{
		out += btoa(ostr_scrambled);
	}
	else
	{
		out += ostr_scrambled;
	}
	prompt("Copy to clipboard: Ctrl+C, Enter", out);
	return out;
}
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
