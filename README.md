<p align="center">
  <a href=#>
    <img src="https://s3.amazonaws.com/intranet-projects-files/holbertonschool-higher-level_programming+/263/HBTN-hbnb-Final.png" alt="Holberton School HBnB logo">
  </a>
</p>

<center>
<h1>HBnB</h1>
<em>Holberton School Air BnB clone</em>
</center>

## Table of Contents
* [About](#about)
    * [Technologies](#technologies)
* [The Console](#the-console)
* [Web Static](#web-static)
* [Authors](#authors)

## About
HBnB is a clone of the Air BnB website. The project is divided into 7 parts:
1. The Console
2. Web Static
3. Database
4. Deploy Static
5. Web Framework
6. REST API
7. Web Dynamic

### Technologies
This project was developed with the following tools:
* **Environment**: Ubuntu 14.04 (Trusty)
* **Codebase**: Python 3.4.3
  * **ORM**: SQLAlchemy
  * **Web Framework**: Flask
* **Linter**: PEP8
* **Database**: MySQL 5.7

## The Console
The Console is the first stage of the HBnB clone. In it, we wrote classes for representing users and listings, a file storage engine for saving and recalling data between interactive sessions, as well as a command interpreter (the console), for easily managing our data. The console provides a backend interface to our storage engine(s).

### HBnB CLI — The command interpreter
The HBnB CLI (command line interpreter) provides a convenient command line interface specifically to manage (add, delete, modify, etc.) HBnB data.
It offers an imporved workflow over alternatives such as embedding data in the source code, manually managing a data file, or using the Python interpreter to manage the data.

### Commands
Bracketed arguments are optional.
* `all [CLASS]` - Show all objects.
* `create CLASS` - Create a new object.
* `destroy CLASS ID` - Destroy a specified instance.
* `help [COMMAND]` - Get information about a command.
* `quit` - Close an interactive session. Also quit with `^-D` or `EOF`.
* `show CLASS ID` - Display a single instance.
* `update CLASS ID ATTRIBUTE VALUE` - Edit attributes of an instance.

### Usage
Start an interactive HBnB CLI session by executing `console.py`:

`./console.py`

If it runs sucessfully, it will display the prompt and await input:

`(hbnb) `

Simply type any valid command(s) listed above. Type `quit` to exit the interactive session.

The HBnB CLI may also be used non-interacively by piping input to it from a shell:

`$ echo "help" | ./console.py`


### Examples
```
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  all  create  destroy  help  quit  show  update

(hbnb) create Place
aba364fd-8b9e-4c4b-b865-8db6a6e9bc03

(hbnb) all
["[Place] (aba364fd-8b9e-4c4b-b865-8db6a6e9bc03) {'created_at': datetime.datetime(2021, 7, 1, 13, 29, 27, 264673), 'id': 'aba364fd-8b9e-4c4b-b865-8db6a6e9bc03', 'updated_at': datetime.datetime(2021, 7, 1, 13, 29, 27, 264832)}"]
(hbnb) 
```

## Web Static
The Web Static part of this project consisted of designing the website HTML and CSS.

## Database
In the Database stage, we built a second storage engine---database storage. This one uses a MySQL database and SQLAlchemy to manage data persistence. We introduced the following environment variables:
* `HBNB_MYSQL_USER`
* `HBNB_MYSQL_PWD`
* `HBNB_MYSQL_HOST`
* `HBNB_MYSQL_DB`
* `HBNB_TYPE_STORAGE`
If `HBNB_TYPE_STORAGE` = `db`, The database storage engine will be use, which depends upon the values of the other environment variables to establish a connection to a database. Consequently, the specified database must exist *and* contain the expected tables. `setup_mysql_dev.sql` sets up a development environment database and user.

Additionally, both storge engines' classes have the same methods implemented to provide seamless toggling between them. The SQLAlchemy ORM required significant additions to our models in order to properly link them to a database.

## Deploy Static
In this stage, we set up an Nginx web server and deployed our static files using Fabric---at least, that was the plan...

## Web Framework
In the Web Framework stage we learned how to set up routes in Flask and create Jinja templates. That allowed us to create dynamic HTML, with data pulled from out database.

## REST API
**COMING SOON**

## Web Dynamic
**COMING COON**

## Bugs
No known bugs. 

## Authors
### V1 authors:
Alexa Orrico - [Github](https://github.com/alexaorrico) / [Twitter](https://twitter.com/alexa_orrico)  
Jennifer Huang - [Github](https://github.com/jhuang10123) / [Twitter](https://twitter.com/earthtojhuang)

### V2 Authors:
Joann Vuong

### V3 Authors;
Justin Masayda [@keysmusician](https://github.com/keysmusician)    
Carson Stearn [@krytech](https://github.com/krytech)

## License
All rights reserved.

