HOST="sub.example.org"

head /dev/urandom > /dev/null
openssl genrsa -rand /dev/urandom -out $HOST.key 2048
openssl req -new -x509 -days 3652 -subj "/C=US/ST=private/L=province/O=city/CN=*.*.$HOST" -key $HOST.key -out $HOST.pem
head /dev/urandom > /dev/null
openssl req -new -newkey rsa:2048 -subj "/C=US/ST=private/L=province/O=city/CN=*.*.$HOST" -rand /dev/urandom -nodes -keyout $HOST.key -out $HOST.csr
openssl x509 -x509toreq -in $HOST.pem -out $HOST.csr -signkey $HOST.key
