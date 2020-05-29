# Rick and Morty Web Application: 

### https://www.rickandmortyapp.co.uk (not running currently)

This Rick and Morty web application is a prototype of a Cloud application developed in Python and Flask where one can use GET, POST, PUT and DELETE methods to interact with the application. It functions as a fun, easy-to-use app which allows its users to access a character catalogue, search for and compare specific characters, test their knowledge of the Rick and Morty TV show and join a community of Rick and Morty fans. It is a REST-based service interface and makes use of an external REST service being the Rick and Morty API (https://rickandmortyapi.com/documentation/) in order to fill the character catalogue and extract the images for the "Test Your Knowledge" game within the applicaiton. The REST API responses conform to REST standards.

Additionally, it makes use of a Cloud database in Apache Cassandra, the free and open-source NoSQL database management system. This is where a table of the characters within the catalogue and the users who have joined the community are stored and managed. See details of set-up below.

Finally, cloud security measures have been implemented. The application is served over HTTPS, with certification granted through EFF's Certbot whilst using the WSGI server Gunicorn along with hash-based authentication where the usernames and hashed passwords are stored in the CQL database. See details of set-up below.

Please use the requirements.txt file for all the packages and specific versions used to build this application.

## Interacting with the Web Application

**Accessing the Root URL**: 
`@app.route('/', methods=['GET'])`

Directs the user to the "Join the Community!" page which allows users to register to the community. Alternatively they can continue to the web application. 

One can make a GET request through the browser with https://www.rickandmortyapp.co.uk or by using the curl command:

```
curl -i -H "Content-Type: application/json" -X GET https://www.rickandmortyapp.co.uk
```

(This just gives you the HTML code used)

This gives the following repsonse code:

```
HTTP/1.1 200 OK
Server: nginx/1.10.3 (Ubuntu)
Date: Tue, 14 Apr 2020 17:34:27 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 1423
Connection: keep-alive
```

**Creating a new user**: 
`@app.route('/new_user_browser', methods=['POST'])`
`@app.route('/new_user_curl', methods=['POST'])`

Posts a new user and their hashed password to the Cassandra database *rickandmortycharacters.users*. Must specify the desired username and password.

One can make a POST request through the browser with https://www.rickandmortyapp.co.uk and enter the username and password into the form where it will execute the app route `/new_user_browser`. Or one can use the curl command:

```
curl -i -H "Content-Type: application/json" -X POST -d '{"username":"example@email.com", "password":"12345"}' https://www.rickandmortyapp.co.uk/new_user_curl
```

This gives the following repsonse code:

```
HTTP/1.1 201 CREATED
Server: nginx/1.10.3 (Ubuntu)
Date: Tue, 14 Apr 2020 22:27:51 GMT
Content-Type: application/json
Content-Length: 46
Connection: keep-alive
```

**Deleting an existing user**:
`@app.route('/delete_user', methods=['DELETE'])`

Deletes an existing username and the hashed password from the Cassandra database rickandmortycharacters.users. The desired username and password for deletion must be specified.

One can make a DELETE request by using the curl command:

```
curl -i -H "Content-Type: application/json" -X DELETE -d '{"username":"example@email.com"}' https://www.rickandmortyapp.co.uk/delete_user
```

This gives the following repsonse code:

```
HTTP/1.1 200 OK
Server: nginx/1.10.3 (Ubuntu)
Date: Tue, 14 Apr 2020 22:47:39 GMT
Content-Type: application/json
Content-Length: 51
Connection: keep-alive
```

**Accessing the home page**:
`@app.route('/home', methods=['GET'])`

Directs users to the home page with a welcome message for users of this web application. Also acts as an index directing users to various services in the app.

One can make a GET request through the browser with https://www.rickandmortyapp.co.uk/home or by using the curl command:

```
curl -i -H "Content-Type: application/json" -X GET https://www.rickandmortyapp.co.uk/home
```

(This just gives you the HTML code used)

This gives the following repsonse code:

```
HTTP/1.1 200 OK
Server: nginx/1.10.3 (Ubuntu)
Date: Tue, 14 Apr 2020 19:55:42 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 3639
Connection: keep-alive
```

**Populating the character catalogue**:
`@app.route('/populate_catalogue', methods=['POST'])`

Populates the catalogue with characters from the external API: https://rickandmortyapi.com/documentation/.

One can make request through the curl command:

```
curl -i -H "Content-Type: application/json" -X POST https://www.rickandmortyapp.co.uk/populate_catalogue
```

This gives the following repsonse code:

```
HTTP/1.1 201 CREATED
Server: nginx/1.10.3 (Ubuntu)
Date: Tue, 14 Apr 2020 20:05:56 GMT
Content-Type: application/json
Content-Length: 73
Connection: keep-alive
```

**Accessing the character catalogue**:
`@app.route('/character_catalogue', methods=['GET'])`

Gets the stats of all the characters in the catalogue filled by the external API database.

One can make a request through the curl command:

```
curl -i -H "Content-Type: application/json" -X GET https://www.rickandmortyapp.co.uk/character_catalogue
```

This gives the following repsonse code:

```
HTTP/1.1 200 OK
Server: nginx/1.10.3 (Ubuntu)
Date: Tue, 14 Apr 2020 20:10:36 GMT
Content-Type: application/json
Content-Length: 77830
Connection: keep-alive
```

**Searching for a specific character in the catalogue**:
`@app.route('/search', methods=['GET'])`
`@app.route('/search/success_browser', methods=['GET', 'POST'])`
`@app.route('/search/success_curl', methods=['GET'])`

Searches for a specified character in the catalogue. The character ID and name must be specified. One can make a GET request to the https://www.rickandmortyapp.co.uk/search and fill in the form to execute the app route `/search/success_browser`. Or one can use the curl command:

```
curl -i -H "Content-Type: application/json" -X GET -d '{"id":1, "name":"Rick Sanchez"}' https://www.rickandmortyapp.co.uk/search/success_curl
```

This gives the following repsonse code:

```
HTTP/1.1 200 OK
Server: nginx/1.10.3 (Ubuntu)
Date: Tue, 14 Apr 2020 20:36:06 GMT
Content-Type: application/json
Content-Length: 154
Connection: keep-alive
```

**Comparing the stats of two specified characters in catalogue**:
`@app.route('/compare', methods=['GET'])`
`@app.route('/compare/success_browser', methods=['GET', 'POST'])`
`@app.route('/compare/success_curl', methods=['GET', 'POST'])`

Compares the stats of two specified characters in the catalogue. Both the desired characters ID's and name's must be specified. 

One can make a GET request to the https://www.rickandmortyapp.co.uk/compare and fill in the form to execute the app route `/compare/success_browser`. Or one can use the curl command:

```
curl -i -H "Content-Type: application/json" -X GET -d '{"id1":1, "name1":"Rick Sanchez", "id2":2, "name2":"Morty Smith"}' https://www.rickandmortyapp.co.uk/compare/success_curl
```

This gives the following repsonse code:

```
HTTP/1.1 200 OK
Server: nginx/1.10.3 (Ubuntu)
Date: Tue, 14 Apr 2020 21:11:12 GMT
Content-Type: application/json
Content-Length: 305
Connection: keep-alive
```

**Testing your knowledge of the Rick and Morty show**:
`@app.route('/test_your_knowledge', methods=['GET'])`

Generates the image of a randomly selected character from the catalogue and then gives the option to reveal the stats by utilising the external Rick and Morty API (https://rickandmortyapi.com/documentation/).

One can make a GET request to the https://www.rickandmortyapp.co.uk/test_your_knowledge and click the "Generate" button and then click the "REVEAL STATS!" button. Or one can use the curl command:

```
curl -i -H "Content-Type: application/json" -X GET https://www.rickandmortyapp.co.uk/test_your_knowledge
```

(This just gives you the HTML code used)

This gives the following repsonse code:

```
HTTP/1.1 200 OK
Server: nginx/1.10.3 (Ubuntu)
Date: Tue, 14 Apr 2020 21:31:12 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 3997
Connection: keep-alive
```

**Adding new characters to the catalogue**:
`@app.route('/character', methods=['POST'])`

Posts a new character to the catalogue. The desired character ID and name must be specified.

One can make a POST request by using the curl command:

```
curl -i -H "Content-Type: application/json" -X POST -d '{"id":494, "name":"Dummy Character"}' https://www.rickandmortyapp.co.uk/character
```

This gives the following repsonse code:

```
HTTP/1.1 201 CREATED
Server: nginx/1.10.3 (Ubuntu)
Date: Tue, 14 Apr 2020 21:53:27 GMT
Content-Type: application/json
Content-Length: 54
Connection: keep-alive
```

**Modifying a character's gender**:
`@app.route('/character/update_gender', methods=['PUT'])`

Updates the gender of an existing character. The desired character ID and name along with the gender you would like to modify it to must be specified.

One can make a PUT request by using the curl command:

```
curl -i -H "Content-Type: application/json" -X PUT -d '{"id":494, "name":"Dummy Character", "gender":"Male"}' https://www.rickandmortyapp.co.uk/character/update_gender
```

(This just gives you the HTML code used)

This gives the following repsonse code:

```
HTTP/1.1 200 OK
Server: nginx/1.10.3 (Ubuntu)
Date: Tue, 14 Apr 2020 22:03:17 GMT
Content-Type: application/json
Content-Length: 53
Connection: keep-alive
```

**Modifying a character's species**:
`@app.route('/character/update_species', methods=['PUT'])`

Updates the species of an existing character. The desired character ID and name along with the species you would like to modify it to must be specified.

One can make a PUT request by using the curl command:

```
curl -i -H "Content-Type: application/json" -X PUT -d '{"id":494, "name":"Dummy Character", "species":"Human"}' https://www.rickandmortyapp.co.uk/character/update_species
```

(This just gives you the HTML code used)

This gives the following repsonse code:

```
HTTP/1.1 200 OK
Server: nginx/1.10.3 (Ubuntu)
Date: Tue, 14 Apr 2020 22:10:00 GMT
Content-Type: application/json
Content-Length: 53
Connection: keep-alive
```

**Modifying a character's status**:
`@app.route('/character/update_status', methods=['PUT'])`

Updates the status of an existing character. The desired character ID and name along with the status you would like to modify it to must be specified.

One can make a PUT request by using the curl command:

```
curl -i -H "Content-Type: application/json" -X PUT -d '{"id":494, "name":"Dummy Character", "status":"Alive"}' https://www.rickandmortyapp.co.uk/character/update_status
```

(This just gives you the HTML code used)

This gives the following repsonse code:

```
HTTP/1.1 200 OK
Server: nginx/1.10.3 (Ubuntu)
Date: Tue, 14 Apr 2020 22:17:57 GMT
Content-Type: application/json
Content-Length: 53
Connection: keep-alive
```

**Deleting existing characters from the catalogue**:
`@app.route('/character', methods=['DELETE'])`

Deletes the character the user wishes to delete from the catalogue. The desired character ID and name must be specified.

One can make a DELETE request by using the curl command:

```
curl -i -H "Content-Type: application/json" -X DELETE -d '{"id":494, "name":"Dummy Character"}' https://www.rickandmortyapp.co.uk/character
```

This gives the following repsonse code:

```
HTTP/1.1 200 OK
Server: nginx/1.10.3 (Ubuntu)
Date: Tue, 14 Apr 2020 22:23:09 GMT
Content-Type: application/json
Content-Length: 54
Connection: keep-alive
```



## Deploying Cassandra via Docker

Pull the Cassandra Docker Image:

```
sudo docker pull cassandra:latest
```

Run a Cassandra instance within docker:

```
sudo docker run --name cassandra-miniproject -p 9042:9042 -d cassandra:latest
```

Interact with Cassandra via its native command line shell client called ‘cqlsh’ using CQL:

```
  sudo docker exec -it cassandra-miniproject cqlsh
```

 Within the Cassandra terminal, create a keyspace for the data to be inserted into:

```CQL
CREATE KEYSPACE rickandmortycharacters WITH REPLICATION =
{'class' : 'SimpleStrategy', 'replication_factor' : 1};
```

Create the table inside of the keyspace, specifying all column names and types, firstly for the catalogue of characters and secondly for the users who sign up as part of the community:

```CQL
CREATE TABLE rickandmortycharacters.catalogue (ID int, Name text, Gender text, Species text, Status text, Image_url text, PRIMARY KEY ((ID), Name));
```

```CQL
CREATE TABLE rickandmortycharacters.users (Username text PRIMARY KEY, Password text);
```

Then populate `rickandmortycharacters.catalogue` using the curl command stated in the section above:

```
curl -i -H "Content-Type: application/json" -X POST https://www.rickandmortyapp.co.uk/populate_catalogue
```



## Implementing hash-based authentication

In the MiniProjectApp.py file, import the library Werkzeug:

```python
from werkzeug.security import generate_password_hash
```

One can use the `generate_password_hash` function to hash the password which a user has posted to `rickandmortycharacters.users` using the SHA-256 which generates an almost-unique 256-bit (32-byte) signature:

```python
password = generate_password_hash(request.form['password'], method='sha256')
```

Check what the hashed password looks like in the Cassandra instance in the table `rickandmortycharacters.users`:

```CQL
SELECT password FROM rickandmortycharacters.users WHERE username='example@email.com';

 password
----------------------------------------------------------------------------------
 sha256$eReCsggX$d7e44c846a068022e5bd2d1109a5c2949ef73bac1ceff81c8e7bb3ac3875bc37
```



## Serving the Application over HTTPS

### Nginx and Gunicorn

First, install Nginx as the web server in order to enable HTTPS, along with Gunicorn in order to handle the Python code:

```
sudo apt install nginx
pip3 install gunicorn
```

Remove the default Nginx configuration file and create a new configuration file:

```
sudo rm /etc/nginx/sites-enabled/default
sudo nano /etc/nginx/sites-enabled/flaskminiproject
```

Modify the new configuration file to the following:

```
server {
        server_name www.rickandmortyapp.co.uk;

        location /static {
                alias /home/ubuntu/MiniProject/static;
        }

        location / {
                proxy_pass http://localhost:8000;
                include /etc/nginx/proxy_params;
                proxy_redirect off;
        }
```

Activate Firewall and enable it on system startup, restart the Nginx server and run Gunicorn with number of workers equal to 5 [in the Gunicorn documentation it recommends (2 x $num_cores) + 1 as the number of workers to start off with. Run the command `nproc --all` to check number of cores]:

```
sudo ufw enable
sudo systemctl restart nginx
gunicorn -w 5 MiniProjectApp:app
```

### HTTPS Certificate

Now start to secure the web server and enable HTTPS on the web application by obtaining a free certificate using the Certificate Authority https://letsencrypt.org and the software tool with shell access https://certbot.eff.org/. These are the instructions for a HTTP website running Nginx on Ubuntu 16.04.

Add the Certbot PPA to your list of repositories:

```
sudo apt-get update
sudo apt-get install software-properties-common
sudo add-apt-repository universe
sudo add-apt-repository ppa:certbot/certbot
sudo apt-get update
```

Install Certbot:

```
sudo apt-get install certbot python-certbot-nginx
```

Get a certificate and have Certbot edit your Nginx configuration automatically, turning on HTTPS access:

```
sudo certbot --nginx
```
