from flask import Flask, request, jsonify, render_template, redirect
from werkzeug.security import generate_password_hash
from cassandra.cluster import Cluster
from io import BytesIO
import re
import urllib.request
import json
import requests
import os



cluster = Cluster(contact_points=['127.0.0.1'], port=9042)
session = cluster.connect()

app = Flask(__name__)




'''
DESCRIPTION:	Directs the user to the "Join the Community!" page which allows users to 
				register the community. Alternatively they can continue to the web application. 

REQUEST:	BROWSWER:	https://www.rickandmortyapp.co.uk
			CURL:		curl -i -H "Content-Type: application/json" -X GET https://www.rickandmortyapp.co.uk
'''
@app.route('/', methods=['GET'])
def join_the_community():
    return render_template('join_the_community.html'), 200







'''
DESCRIPTION:	Posts a new user and their hashed password to the Cassandra database rickandmortycharacters.users.	 			

REQUEST:	BROWSER:	https://www.rickandmortyapp.co.uk and enter the username and password into the form.
'''
@app.route('/new_user_browser', methods=['POST'])
def create_new_user_browser():

	username = request.form['username']
	password = generate_password_hash(request.form['password'], method='sha256')
	
	result = session.execute("""SELECT password FROM rickandmortycharacters.users WHERE username='{}'""".format(username))

	if (len(result.current_rows) == 0):
		result = session.execute("""INSERT INTO rickandmortycharacters.users (username, password) VALUES ('{}', '{}')""".format(username, password))

		return redirect('/home'), 201

	else:
		return jsonify({'error':'This email address is already in use. Please press the back button on your browser and choose another email address.'}), 409






'''
DESCRIPTION:	Posts a new user and their hashed password to the Cassandra database rickandmortycharacters.users.
				Must specify the desired username and password.	 
				
REQUEST:		CURL:	curl -i -H "Content-Type: application/json" -X POST -d 
				'{"username":"example@email.com", "password":"12345"}' https://www.rickandmortyapp.co.uk/new_user_curl
'''
@app.route('/new_user_curl', methods=['POST'])
def create_new_user_curl():

	if not request.json or not "username" in request.json or not "password" in request.json:
		return jsonify({'error':'must give a username and password of a user you would like to add'}), 400

	username = request.json['username']
	password = generate_password_hash(request.json['password'], method='sha256')
	
	result = session.execute("""SELECT password FROM rickandmortycharacters.users WHERE username='{}'""".format(username))

	if (len(result.current_rows) == 0):
		result = session.execute("""INSERT INTO rickandmortycharacters.users (username, password) VALUES ('{}', '{}')""".format(username, password))

		return jsonify({'message': 'created user: {}'.format(username)}), 201

	else:
		return jsonify({'error':'This email address is already in use. Please press the back button on your browser and choose another email address.'}), 409






'''
DESCRIPTION:	Deletes an existing username and the hashed password from the Cassandra database rickandmortycharacters.users.
				Must specify the desired username and password for deletion.
				
REQUEST:		curl -i -H "Content-Type: application/json" -X DELETE -d 
				'{"username":"example@email.com"}' https://www.rickandmortyapp.co.uk/delete_user
'''
@app.route('/delete_user', methods=['DELETE'])
def delete_existing_user():

	if not request.json or not "username" in request.json:
		return jsonify({'error':'must give the username you would like to delete'}), 400

	username = request.json['username']

	row_username_count = session.execute( """SELECT COUNT(*) FROM rickandmortycharacters.users WHERE username = '{}' ALLOW FILTERING""".format(username))

	if row_username_count[0][-1] == 0:
		return jsonify({'error': 'the username you wish to delete does not exist'}), 404

	session.execute( """DELETE FROM rickandmortycharacters.users WHERE username='{}'""".format(username))
	return jsonify({'message': 'deleted: /username/{}'.format(username)}), 200







'''
DESCRIPTION:	Directs users to the home page with welcome message for users of this web application.
				Also acts as an index directing users to various services in the app.

REQUEST:	BROWSER:	https://www.rickandmortyapp.co.uk/home	
			CURL:		curl -i -H "Content-Type: application/json" -X GET https://www.rickandmortyapp.co.uk/home
'''
@app.route('/home', methods=['GET'])
# @login_required
def welcome():
	return render_template("index.html")







'''
DESCRIPTION:	Populates the catalogue with characters from the external API: https://rickandmortyapi.com/documentation/

REQUEST:	CURL: 	curl -i -H "Content-Type: application/json" -X POST https://www.rickandmortyapp.co.uk/populate_catalogue
'''
@app.route('/populate_catalogue', methods=['POST'])
def populate_catalogue_external_API():

	RickAndMorty_url_template = 'https://rickandmortyapi.com/api/character/?page={page_number}'

	# my_page_number = int(request.json['page_number'])

	characters = []

	for page in range(1,26):
		RickAndMorty_url = RickAndMorty_url_template.format(page_number = page)
		resp = requests.get(RickAndMorty_url)
		if resp.ok:
			characters.append(resp.json())

	# ID = characters[0]						#gets the first page
	# ID = characters[0]['results']  			#gets the results from first page
	# ID = characters[0]['results'][0]  		#gets the first character

	# ID = characters[0]['results'][0]['id']	#gets the id of the first character

	# NAME = characters[0]['results'][0]['name']
	# GENDER = characters[0]['results'][0]['gender']
	# SPECIES = characters[0]['results'][0]['species']
	# STATUS = characters[0]['results'][0]['status']
	# IMAGE = characters[0]['results'][0]['image']

	ID = []
	NAME = []
	GENDER = []
	SPECIES = []
	STATUS = []
	IMAGE = []

	for i in range(0,24):
		ID_1 = characters[i]['results']
		NAME_1 = characters[i]['results']
		GENDER_1 = characters[i]['results']
		SPECIES_1 = characters[i]['results']
		STATUS_1 = characters[i]['results']
		IMAGE_1 = characters[i]['results']
		for j in range(0,20):    
			ID.append(ID_1[j]['id'])
			NAME.append(NAME_1[j]['name'])
			GENDER.append(GENDER_1[j]['gender'])
			SPECIES.append(SPECIES_1[j]['species'])
			STATUS.append(STATUS_1[j]['status'])
			IMAGE.append(IMAGE_1[j]['image'])

	# FOR LAST PAGE WHERE THERE ARE ONLY 14 CHARACTER ENTRIES
	ID_2 = characters[24]['results']
	NAME_2 = characters[24]['results']
	GENDER_2 = characters[24]['results']
	SPECIES_2 = characters[24]['results']
	STATUS_2 = characters[24]['results']
	IMAGE_2 = characters[24]['results']
	for j in range(0,13):		# (0,14) is out of range for last page
		ID.append(ID_2[j]['id'])
		NAME.append(NAME_2[j]['name'])
		GENDER.append(GENDER_2[j]['gender'])
		SPECIES.append(SPECIES_2[j]['species'])
		STATUS.append(STATUS_2[j]['status'])
		IMAGE.append(IMAGE_2[j]['image'])
	
	for i in range(0,493):
		NAME[i] = NAME[i].replace("'", "")
		NAME[i] = NAME[i].replace(".", "")

	# return jsonify({'id':ID, 'name':NAME, 'gender':GENDER, 'species':SPECIES, 'status':STATUS, 'image':IMAGE})

	for i in range(0,493):
		session.execute("""INSERT INTO rickandmortycharacters.catalogue(id, name, gender, species, status, image_url) \
			VALUES( {}, '{}', '{}', '{}', '{}', '{}')""".format(int(ID[i]), NAME[i], GENDER[i], SPECIES[i], STATUS[i], IMAGE[i]))

	return jsonify({'message':'catalogue filled with character from external API database'}), 201







''' 
DESCRIPTION: 		Gets the stats of all the characters in the catalogue filled by the external API database.

REQUEST:	CURL:	curl -i -H "Content-Type: application/json" -X GET https://www.rickandmortyapp.co.uk/character_catalogue
'''
@app.route('/character_catalogue', methods=['GET'])
def get_all_characters():

	rows = session.execute( """SELECT * FROM rickandmortycharacters.catalogue""")
	result = []

	for r in rows:
		result.append({"id":r.id, "name":r.name, "gender":r.gender, "species":r.species, "status":r.status, "image_url":r.image_url})
	
	return jsonify(result), 200






''' 
DESCRIPTION:		Directs user to the "Search for a Specific Character" page.					

REQUEST:	BROWSER:	https://www.rickandmortyapp.co.uk/search
'''
@app.route('/search', methods=['GET'])
def search_characters():
	return render_template('search.html'), 200






''' 
DESCRIPTION: 		Searches for a specified character in the catalogue.
					Must specify both the character id and name.

REQUEST:	BROWSER:	https://www.rickandmortyapp.co.uk/search
'''
@app.route('/search/success_browser', methods=['GET', 'POST'])
def search_characters_browser():

	ID = request.form['character_id']
	name = request.form['character_name']

	row_name_count = session.execute( """SELECT COUNT(*) FROM rickandmortycharacters.catalogue WHERE id = {} AND name = '{}' ALLOW FILTERING""".format(ID,name))

	row_name = session.execute( """SELECT * FROM rickandmortycharacters.catalogue WHERE id= {} AND name = '{}' ALLOW FILTERING""".format(ID,name))
	
	result = []

	if (row_name_count[0][-1] == 0):
		return jsonify(\
			{'error': 'the character id and name you wish to select does not exist in this catalogue or the id and name do not match - Please check the character catalogue and try again.'})\
		, 404
	
	else:
		for r in row_name:
			result.append({"id":r.id, "name":r.name, "gender":r.gender, "species":r.species, "status":r.status, "image_url":r.image_url})

		return jsonify(result), 200






''' 
DESCRIPTION: 		Searches for a specified character in the catalogue.
					Must specify both the character id and name.

REQUEST:	CURL:	curl -i -H "Content-Type: application/json" -X GET -d '{"id":1, "name":"Rick Sanchez"}' https://www.rickandmortyapp.co.uk/search/success_curl
'''
@app.route('/search/success_curl', methods=['GET'])
def search_characters_curl():

	if not request.json or not "id" in request.json or not "name" in request.json:
		return jsonify({'error':'must give the name of the character you wish to select'}), 400

	ID = request.json['id']
	name = request.json['name']

	row_name_count = session.execute( """SELECT COUNT(*) FROM rickandmortycharacters.catalogue WHERE id = {} AND name = '{}' ALLOW FILTERING""".format(ID,name))

	row_name = session.execute( """SELECT * FROM rickandmortycharacters.catalogue WHERE id= {} AND name = '{}' ALLOW FILTERING""".format(ID,name))
	
	result = []

	if (row_name_count[0][-1] == 0):
		return jsonify(\
			{'error': 'the character id and name you wish to select does not exist in this catalogue or the id and name do not match - Please check the character catalogue and try again.'})\
		, 404
	
	else:
		for r in row_name:
			result.append({"id":r.id, "name":r.name, "gender":r.gender, "species":r.species, "status":r.status, "image_url":r.image_url})

		return jsonify(result), 200







''' 
DESCRIPTION:		Directs user to the "Compare Two Character's" page.					

REQUEST:	BROWSER:	https://www.rickandmortyapp.co.uk/compare
'''
@app.route('/compare', methods=['GET'])
def compare_characters():
	return render_template('compare.html'), 200








''' 
DESCRIPTION: 		Compares the stats two specified characters in the catalogue.
					Must specify both the character id and name.

REQUEST:	BROWSER:	https://www.rickandmortyapp.co.uk/search
'''
@app.route('/compare/success_browser', methods=['GET', 'POST'])
def compare_characters_browser():

	ID1 = request.form['character_id1']
	name1 = request.form['character_name1']
	ID2 = request.form['character_id2']
	name2 = request.form['character_name2']

	row_name1_count = session.execute( """SELECT COUNT(*) FROM rickandmortycharacters.catalogue WHERE id = {} AND name = '{}' ALLOW FILTERING""".format(ID1,name1))
	row_name2_count = session.execute( """SELECT COUNT(*) FROM rickandmortycharacters.catalogue WHERE id = {} AND name = '{}' ALLOW FILTERING""".format(ID2,name2))

	row_name1 = session.execute( """SELECT * FROM rickandmortycharacters.catalogue WHERE id = {} AND name = '{}' ALLOW FILTERING""".format(ID1,name1))
	row_name2 = session.execute( """SELECT * FROM rickandmortycharacters.catalogue WHERE id = {} AND name = '{}' ALLOW FILTERING""".format(ID2,name2))
	
	result = []

	if (row_name1_count[0][-1] == 0) or (row_name2_count[0][-1] == 0):
		return jsonify({'error': 'One or both the character names you wish to compare do not exist in this catalogue'}), 404
	
	else:
		for r in row_name1:
			result.append({"id":r.id, "name":r.name, "gender":r.gender, "species":r.species, "status":r.status, "image_url":r.image_url})
		for r in row_name2:
			result.append({"id":r.id, "name":r.name, "gender":r.gender, "species":r.species, "status":r.status, "image_url":r.image_url})
		return jsonify(result), 200







''' 
DESCRIPTION: 		Compares the stats two specified characters in the catalogue.
					Must specify both the character id and name.

REQUEST:	CURL:	curl -i -H "Content-Type: application/json" -X GET -d 
					'{"id1":1, "name1":"Rick Sanchez", "id2":2, "name2":"Morty Smith"}' https://www.rickandmortyapp.co.uk/compare/success_curl
'''
@app.route('/compare/success_curl', methods=['GET'])
def compare_characters_curl():
	if not request.json or not "name1" in request.json or not "name2" in request.json or not "id1" in request.json or not "id2" in request.json:
		return jsonify({'error':'must give the IDs and names of both the characters you wish to compare'}), 400

	ID1 = request.json['id1']
	name1 = request.json['name1']
	ID2 = request.json['id2']
	name2 = request.json['name2']

	row_name1_count = session.execute( """SELECT COUNT(*) FROM rickandmortycharacters.catalogue WHERE id = {} AND name = '{}' ALLOW FILTERING""".format(ID1,name1))
	row_name2_count = session.execute( """SELECT COUNT(*) FROM rickandmortycharacters.catalogue WHERE id = {} AND name = '{}' ALLOW FILTERING""".format(ID2,name2))

	row_name1 = session.execute( """SELECT * FROM rickandmortycharacters.catalogue WHERE id = {} AND name = '{}' ALLOW FILTERING""".format(ID1,name1))
	row_name2 = session.execute( """SELECT * FROM rickandmortycharacters.catalogue WHERE id = {} AND name = '{}' ALLOW FILTERING""".format(ID2,name2))

	result = []

	if (row_name1_count[0][-1] == 0) or (row_name2_count[0][-1] == 0):
		return jsonify({'error': 'One or both the character names you wish to compare do not exist in this catalogue'}), 404
	
	else:
		for r in row_name1:
			result.append({"id":r.id, "name":r.name, "gender":r.gender, "species":r.species, "status":r.status, "image_url":r.image_url})
		for r in row_name2:
			result.append({"id":r.id, "name":r.name, "gender":r.gender, "species":r.species, "status":r.status, "image_url":r.image_url})
		return jsonify(result), 200







''' 
DESCRIPTION: 		Gives image of randomly selected character and reveals stats.

REQUEST:	BROWSER:	https://www.rickandmortyapp.co.uk/test_your_knowledge
'''
@app.route('/test_your_knowledge', methods=['GET'])
def random_image_generator_and_reveal():

	######################################################
	#### OPTIONAL: SAVE IMAGE .JPEG FILES TO INSTANCE ####
	######################################################
	# rows = session.execute( """SELECT name, image_url FROM rickandmortycharacters.catalogue""")
	# result = []
	# images = []

	# for r in rows:
	# 	result.append((r.name, r.image_url))
	# 	images.append(r.image_url)

	# def atoi(text):
	# 	return int(text) if text.isdigit() else text
	# def natural_keys(text):
	#     return [ atoi(c) for c in re.split(r'(\d+)', text) ]		
	# images.sort(key=natural_keys)	
	# count = 0
	# for i in images:
	# 	count += 1
	# 	filename = 'characterimage-{}.jpg'.format(count)
	# 	full_path = 'img/{}'.format(filename)
	# 	urllib.request.urlretrieve(i, full_path)
	######################################################
	######################################################

	return render_template("generator.html")








'''
DESCRIPTION:	Posts a new character to the catalogue.
				Must specify the character ID and name.

REQUEST:	CURL:	curl -i -H "Content-Type: application/json" -X POST -d 
					'{"id":494, "name":"Dummy Character"}' https://www.rickandmortyapp.co.uk/character
'''
@app.route('/character', methods=['POST'])
def create_new_character():

	if not request.json or not "id" in request.json or not "name" in request.json:
		return jsonify({'error':'must give a id and name of a character you would like to add'}), 400

	ID = int(request.json['id'])
	name = request.json['name']

	row_id_count = session.execute( """SELECT COUNT(*) FROM rickandmortycharacters.catalogue WHERE id = {} ALLOW FILTERING""".format(ID))
	row_name_count = session.execute( """SELECT COUNT(*) FROM rickandmortycharacters.catalogue WHERE name = '{}' ALLOW FILTERING""".format(name))
	
	if (row_name_count[0][-1] != 0) or (row_id_count[0][-1] != 0):
		#return jsonify({'counts': 'name_count:{} id_count:{}'.format(row_name_count[0][-1], row_id_count[0][-1])}), 409
		return jsonify({'error': 'The ID number or character name already exists in this catalogue'}), 409
	else:
		session.execute("""INSERT INTO rickandmortycharacters.catalogue(id, name) VALUES( {}, '{}')""".format(ID, name))
		return jsonify({'message': 'created: /character/{}_{}'.format(ID, name)}), 201
		






'''
DESCRIPTION: 	Updates the gender of an existing character.
				Must specify the character ID and name along with the gender you would like to modify it to.

REQUEST:	CURL:	curl -i -H "Content-Type: application/json" -X PUT -d 
					'{"id":494, "name":"Dummy Character", "gender":"Male"}' https://www.rickandmortyapp.co.uk/character/update_gender
'''
@app.route('/character/update_gender', methods=['PUT'])
def update_character_gender():

	if not request.json or not "gender" in request.json or not "id" in request.json or not "name":
		return jsonify({'error':' You must enter the updated gender and the character id and name you wish to update'}), 400

	gender = request.json['gender']

	ID = int(request.json['id'])
	name = request.json['name']

	row_id_count = session.execute( """SELECT COUNT(*) FROM rickandmortycharacters.catalogue WHERE id = {} ALLOW FILTERING""".format(ID))
	row_name_count = session.execute( """SELECT COUNT(*) FROM rickandmortycharacters.catalogue WHERE name = '{}' ALLOW FILTERING""".format(name))
	
	if (row_name_count[0][-1] == 0) or (row_id_count[0][-1] == 0):
		#return jsonify({'counts': 'name_count:{} id_count:{}'.format(row_name_count[0][-1], row_id_count[0][-1])}), 404
		return jsonify({'error': 'the character id or name you wish to update does not exist in this catalogue'}), 404

	session.execute( """UPDATE rickandmortycharacters.catalogue SET gender='{}' WHERE id={} AND name='{}'""".format(gender, ID, name))
	return jsonify({'message': 'updated gender: /character/{}_{}'.format(ID, name)}), 200






'''
DESCRIPTION: 	Updates the species of an existing character.
				Must specify the character ID and name along with the species you would like to modify it to.

REQUEST:	CURL:	curl -i -H "Content-Type: application/json" -X PUT -d 
					'{"id":494, "name":"Dummy Character", "species":"Human"}' https://www.rickandmortyapp.co.uk/character/update_species
'''
@app.route('/character/update_species', methods=['PUT'])
def update_character_species():

	if not request.json or not "species" in request.json or not "id" in request.json or not "name":
		return jsonify({'error':' You must enter the updated species and the character id and name you wish to update'}), 400

	species = request.json['species']

	ID = int(request.json['id'])
	name = request.json['name']

	row_id_count = session.execute( """SELECT COUNT(*) FROM rickandmortycharacters.catalogue WHERE id = {} ALLOW FILTERING""".format(ID))
	row_name_count = session.execute( """SELECT COUNT(*) FROM rickandmortycharacters.catalogue WHERE name = '{}' ALLOW FILTERING""".format(name))
	
	if (row_name_count[0][-1] == 0) or (row_id_count[0][-1] == 0):
		#return jsonify({'counts': 'name_count:{} id_count:{}'.format(row_name_count[0][-1], row_id_count[0][-1])}), 404
		return jsonify({'error': 'the character id or name you wish to update does not exist in this catalogue'}), 404

	session.execute( """UPDATE rickandmortycharacters.catalogue SET species='{}' WHERE id={} AND name='{}'""".format(species, ID, name))
	return jsonify({'message': 'updated species: /character/{}_{}'.format(ID, name)}), 200







'''
DESCRIPTION: 	Updates the status of an existing character.
				Must specify the character ID and name along with the status you would like to modify it to.

REQUEST:	CURL:	curl -i -H "Content-Type: application/json" -X PUT -d 
					'{"id":494, "name":"Dummy Character", "status":"Alive"}' https://www.rickandmortyapp.co.uk/character/update_status
'''
@app.route('/character/update_status', methods=['PUT'])
def update_character_status():

	if not request.json or not "status" in request.json or not "id" in request.json or not "name":
		return jsonify({'error':' You must enter the updated status and the character id and name you wish to update'}), 400

	status = request.json['status']

	ID = int(request.json['id'])
	name = request.json['name']

	row_id_count = session.execute( """SELECT COUNT(*) FROM rickandmortycharacters.catalogue WHERE id = {} ALLOW FILTERING""".format(ID))
	row_name_count = session.execute( """SELECT COUNT(*) FROM rickandmortycharacters.catalogue WHERE name = '{}' ALLOW FILTERING""".format(name))
	
	if (row_name_count[0][-1] == 0) or (row_id_count[0][-1] == 0):
		#return jsonify({'counts': 'name_count:{} id_count:{}'.format(row_name_count[0][-1], row_id_count[0][-1])}), 404
		return jsonify({'error': 'the character id or name you wish to update does not exist in this catalogue'}), 404

	session.execute( """UPDATE rickandmortycharacters.catalogue SET status='{}' WHERE id={} AND name='{}'""".format(status, ID, name))
	return jsonify({'message': 'updated status: /character/{}_{}'.format(ID, name)}), 200







'''
DESCRIPTION: 	Deletes the character the user wishes to delete from the catalogue.
				Must enter both ID and name of desired character.

REQUEST:	CURL:	curl -i -H "Content-Type: application/json" -X DELETE -d '{"id":494, "name":"Dummy Character"}' https://www.rickandmortyapp.co.uk/character
'''
@app.route('/character', methods=['DELETE'])
def delete_existing_character():

	if not request.json or not "id" in request.json or not "name" in request.json:
		return jsonify({'error':'must give the id and name of the character you wish to delete'}), 400

	ID = int(request.json['id'])
	name = request.json['name']
	

	row_id_count = session.execute( """SELECT COUNT(*) FROM rickandmortycharacters.catalogue WHERE id = {} ALLOW FILTERING""".format(ID))
	row_name_count = session.execute( """SELECT COUNT(*) FROM rickandmortycharacters.catalogue WHERE name = '{}' ALLOW FILTERING""".format(name))


	if (row_id_count[0][-1] == 0) or (row_name_count[0][-1] == 0):
		return jsonify({'error': 'the character id or name you wish to delete does not exist in this catalogue'}), 404

	session.execute( """DELETE FROM rickandmortycharacters.catalogue WHERE id={}""".format(ID))
	return jsonify({'message': 'deleted: /character/{}_{}'.format(ID, name)}), 200








if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)