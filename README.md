# Mirage: For all your market research needs

This project is in the very early stages. Right now it's a basic Django project. You can get started by:

 * Installing PostgreSQL (installation guides [here](https://wiki.postgresql.org/wiki/Detailed_installation_guides))
 * Installing virtualenv and creating a virtual environment
 * Installing the python requirements with ```pip install -r requirements.txt```
 * Creating a postgresql database and storing the settings in a ```local_settings.py``` file, a sibling of ```settings.py```
 * Run ```manage.py syncdb```
 * Run `manage.py runserver` to start the server



Next you'll need to load data so that you have something to query. Inside the `/vendor/fixtures/` directory you can find several fixtures to get you started. You can load these using the `loaddata` manage command like so:

`manage.py loaddata vendor/fixtures/naics.json`

Make sure to load naics.json, pools.json, and setasides.json (in that order).

Now you can run the ```load_vendors``` manage command to get the most up-to-date information.

```manage.py load_vendors```

Note that this manage command requires you to specify a ```SAM_API_KEY``` variable in your local settings file as shown in local_settings.example.py. This value should be a valid Data.gov API key. The loader runs slightly faster than the rate limiting on api.data.gov, so you'll need to lift that limit on your key. Contact the OASIS development team for details. 

Once the server is started you can query the api at
`http://localhost:8000/api/vendors/`

Providing no query parameters will return all vendors. However you can also filter by NAICS shortcode or by setaside code.

For example:
`http://localhost:8000/api/vendors/?setasides=A5,QF&naics=541330`
will return vendors that have the setaside codes A5 and QF and also do business under the NAICS code 541330.

You can also add a `group` parameter to get the vendors grouped by pool, like so:
`http://localhost:8000/api/vendors/?setasides=A5,QF&naics=541330&group=pool`


### Public domain

This project is in the worldwide [public domain](LICENSE.md). As stated in [CONTRIBUTING](CONTRIBUTING.md):

> This project is in the public domain within the United States, and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
>
> All contributions to this project will be released under the CC0 dedication. By submitting a pull request, you are agreeing to comply with this waiver of copyright interest.
