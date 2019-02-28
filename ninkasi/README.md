# Ninkasi
A periodic table of beer styles.  Ninkasi aims to be an Application Programming Interface (API) to provide information of beer styles in JavaScript Object Notation (JSON).  The periodic table used as reference to this project is available at [Bierminen's Facebook page](https://www.facebook.com/bierminen/photos/pb.274724709583898.-2207520000.1467556269./281347498921619/?type=1&theater).

For example, to get information about India Pale Ale, style #30 in Periodic Table of Beer Styles, you could do it:

```
https://ninkasi.bierminen.com/style/30
```

### Dependencies

* Python 3.5
* Header files<sup>1</sup> (packages `python-dev` and `libpq-dev` on Ubuntu)
* pip (package `python3-pip` on Ubuntu)
* PostgreSQL 9.5
* Psycopg2
* Python's Virtualenv
* Flask 0.11
* Flask-SQLAlchemy
* Flask-Script

<sup>1</sup> Required by Psycopg2.

## Installation

Start by installing basic Linux packages --Ninkasi is proudly developed under Linux:

```sh
$ sudo apt install python3 python-dev libpq-dev python3-pip postgresql-9.5 && pip3 install virtualenv
```

Note we haven't used `sudo` in the second command.  Next, setup the password for database user and create the database:

```sh
$ sudo -u postgres psql
> \password
..type and confirm your password --we'll use foobar for example
> CREATE DATABASE ninkasi;
> \q
```

Clone [this](https://github.com/bierminen/ninkasi) repository.

```sh
$ git clone https://github.com/bierminen/ninkasi
$ cd ninkasi
```

Create the virtual environment and install basic Python packages.

```sh
$ ~/.local/bin/virtualenv env
$ source env/bin/activate
(env) $ pip3 install -r requirements.txt --upgrade
```

Ninkasi uses environment variable to define its operational mode.  You can choose between `production` and `development` modes by setting a `NINKASI_MODE` variable like this:

```sh
$ NINKASI_MODE="development"
```

If no mode is set, then the `production` will be taken.  If you want to make this change permanent, put the following line in your `.bashrc` file --assuming you're using Bash:

```sh
export NINKASI_MODE='development'
```

Run Ninkasi with the `initdb` parameter to populate its database:

```sh
$ ./manage.py initdb
```

## Usage

Launch the server:

```sh
$ ./manage.py runserver
```

Open another terminal and try to access the application URI.

```sh
$ curl http://localhost:5000/style/44
```

You should get the response below.

```json
{
  "status": "OK", 
  "styles": [
    {
      "abv_max": 5.7, 
      "abv_min": 4.5, 
      "description": "Medium maltiness. Mild to strong flavor and aroma from American hop varieties. Notable caramel flavor. (Big Time Atlas Amber, Bell's Amber, North Coast Red Seal Ale)", 
      "fg_max": 1.016, 
      "fg_min": 1.008, 
      "ibu_max": 40, 
      "ibu_min": 20, 
      "name": "American Amber Ale", 
      "number": 44, 
      "og_max": 1.056, 
      "og_min": 1.043, 
      "srm_max": 18, 
      "srm_min": 11, 
      "subtype": "Pale Ale", 
      "type": "Ale"
    }
  ]
}
```

If you want to list all styles, just use this URI: `http://localhost:5000/style`.

## Project Pattern

```
ninkasi/
    /app/
        /__init__.py
        /database.py
        /models.py
        /initdb.py
        /config.py
        /queries.py
        /views.py
        /templates/
            /index.html
    /README.md
    /LICENSE
    /requirements.txt
    /manage.py
```

## About Ninkasi

According to [Wikipedia](https://en.wikipedia.org/wiki/Ninkasi), Ninkasi is the ancient Sumerian tutelary goddess of beer.

Her father was the King of Uruk, and her mother was the high priestess of the temple of Ishtar, or the goddess of procreation.  She is also one of the eight children created in order to heal one of the eight wounds that Enki receives.  Furthermore, she is the goddess of alcohol.  She was also borne of "sparkling fresh water." She is the goddess made to "satisfy the desire" and "sate the heart."  She would prepare the beverage daily.

This project was conceived by José Lopes as part of his brewing project, [Bierminen](https://bierminen.com).  Join us on [Facebook](https://facebook.com/bierminen).

[Bierminen](https://bierminen.com): Zug von verrükten!

Cheers!

Prost!

Saúde!

