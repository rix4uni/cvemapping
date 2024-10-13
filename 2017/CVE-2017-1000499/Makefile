
create:
	docker network create asgard5
	docker run -d --name asgard-mysql571 --network asgard5 -e MYSQL_ROOT_PASSWORD="root" -p 3306:3306 mysql:5.7
	docker run -d     --name asgard-phpmyadmin41     --network asgard5     -e PMA_HOST=asgard-mysql571     -p 80:80 phpmyadmin/phpmyadmin:4.7.6-1
clean:
	docker rm -f asgard-phpmyadmin41
	docker rm -f asgard-mysql571
	docker network rm asgard5
.ONESHELL:
