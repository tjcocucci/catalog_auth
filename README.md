To deploy on localhost, run the following:

1. Create a network
```bash
docker network create auth-service
```
2. Create a volume
```bash
docker volume create auth-service-db
```
3. Run the MySQL container
```bash
docker run --name auth-db-container \
    --network=videoclub-network \
    -e MYSQL_ROOT_PASSWORD=<password> \
    -p 3307:3306 \
    -v auth-service-db:/var/lib/mysql \
    mysql
```
4. Create the database
```bash
docker exec -it auth-db-container mysql -u root -p
```
```sql
CREATE DATABASE auth;
```
5. Run the Auth Service container
```bash
sudo docker run -it --name auth-api-conainer \
    --network=host \
    -p 4000:4000 \
    auth-api-image
```