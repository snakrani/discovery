# Mirage: For all your market research needs

This project is in the very early stages. Right now it's a basic Django project. You can get started by:

 * Installing PostgreSQL (installation guides [here](https://wiki.postgresql.org/wiki/Detailed_installation_guides))
 * Installing virtualenv and creating a virtual environment
 * Installing the python requirements with ```pip install -r requirements.txt```
 * Creating a postgresql database and storing the settings in a ```local_settings.py``` file, a sibling of ```settings.py```
 * Run ```manage.py syncdb```
 * Run `manage.py runserver` to start the server 
 
 Once the server is started you can query the api at
 `http://localhost:8000/api/vendors/`
 
 Providing no query parameters will return all vendors. However you can also filter by NAICS shortcode or by setaside code.
 
 For example:
 `http://localhost:8000/api/vendors/?setasides=A5,QF&naics=541330`
 will return vendors that have the setaside codes A5 and QF and also do business under the NAICS code 541330..



