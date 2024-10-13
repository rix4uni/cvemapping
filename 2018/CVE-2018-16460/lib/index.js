
var cp = require('child_process');

module.exports = exports = function(args, callback) {
	if (Array.isArray(args)) {
		args = args.join(' ');
	}
	cp.exec('ps ' + args, function(err, stdout, stderr) {
		stdout = stdout.toString('utf8');
		stderr = stderr.toString('utf8');
		if (err || stderr) {
			return callback(stderr || err);
		}
		callback(null, stdout.trim() || false);
	});
};

exports.lookup = function(query, callback) {
	var format = query.format;
	
	// Lookup by PID
	if (query.pid) {
		format = parseFormat(format || 'comm pid');

		var pid = Array.isArray(pid)
			? pid.join(',')
			: query.pid;

		return exports([ '-p', pid, '-o', format ], function(err, output) {
			if (err) {
				return callback(err);
			}
			if (query.parse) {
				output = parseGrid(output);
			}
			callback(null, output);
		});
	}

	// Lookup by PPID
	if (query.ppid) {
		format = format || 'comm pid ppid';
		columns = format.split(' ');
		format = parseFormat(format);

		// Parsing is required for ppid queries as we do the filtering internally
		if (query.parse === void(0)) {
			query.parse = true;
		}
		if (! query.parse) {
			throw new Error('ps: the `parse` option cannot be false for ppid queries');
		}

		var ppid = Array.isArray(query.ppid)
			? query.ppid.join(',')
			: query.ppid;

		return exports([ '-p', ppid, '-o', format ], function(err, output) {
			if (err) {
				return callback(err);
			}

			output = parseGrid(output);
			var ppidIndex = columns.indexOf('ppid');

			var ppids = query.ppid;
			if (typeof ppids === 'string') {
				ppids = query.ppid.split(',');
			}
			if (typeof ppids === 'number') {
				ppids = [ ppids ];
			}

			ppids = ppids.map(String);
			output = output.filter(function(line) {
				return (ppids.indexOf(line[ppidIndex]) >= 0);
			});

			callback(null, output);
		});
	}
};

// ------------------------------------------------------------------

function parseGrid(output) {
	if (! output) {return output;}
	return output.split('\n').map(function(line) {
		var returnedOutput = [ ];
		line.split(/\s+/).forEach(function(item) {
			if (item) {
				returnedOutput.push(item);
			}
		});
		return returnedOutput;
	});
}

function parseFormat(format) {
	if (typeof format === 'string') {
		format = format.split(' ');
	}
	format = format.map(function(item) {
		return item + '=';
	});
	return format.join(' -o ');
}

