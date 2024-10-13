# ps

A Node.js module for looking up running processes.

## Install

```bash
$ npm install ps
```

## Usage

```javascript
var ps = require('ps');

// A simple pid lookup
ps.lookup({ pid: 12345 }, function(err, proc) {
    if (err) {throw err;}
    if (proc) {
        console.log(proc);  // Process name, something like "node" or "bash"
    } else {
        console.log('No such process');
    }
});

// Lookup processes in a list of pids and format them
var query = {
    pid: [123, 234, 345],  // Look up these pids
    format: 'pid comm',    // Retrieve the pid and name, like running `ps -o pid= -o comm=`
    parse: true            // Parse the output results into a 2D array
};
ps.lookup(query, function(err, results) {
    if (err) {throw err;}
    if (results) {
        results.forEach(function(proc) {
            console.log('PID: ' + proc[0] + '; Name: ' + proc[1]);
        });
    }
});
```

