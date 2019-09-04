# **DSC Portal App Beta**
### Installation for Front-end dependencies:
The front end is pure CSS, using SASS as a pre-processor

### Install nodejs and npm on your system

#### Arch/Manjaro Base

```console
$ pacman -S nodejs npm
```
#### Debian/Ubuntu Base
```
$ sudo apt update
$ sudo apt install nodejs
$ sudo apt install npm
```
#### Mac OSX
Install Home brew
```
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
$ brew install node
```
---

#### In project root folder run the following command to install dependencies
```
$ npm install
```
#### Then run the next two commands in the project root folder in seperate or tabbed terminals
```
$ npm run compile:sass
```
#### The only caveat to this is you only need to run the compile:sass command if you plan on making changes to the code


### Installation for Back-end dependencies:
This application is using Python/Django as the backend language, Postgres for the database, and relies on Google api's for google sheets/drive integration

---

### Make sure you have a python installation on your system >= 3.6
### Install pip, virtual-env and postgres dev libraries

#### Debian/Ubuntu base
```
$ sudo apt install python3-pip
$ sudo apt install python3-venv
$ sudo apt install libpq-dev
```

### In the project root folder, create a virtual environment, activate it, and install all dependencies via requirements.txt

```
$ python3 -m venv .env
$ source .env/bin/activate
$ pip3 install -r requirements.txt
```

### Django specific commands are next to manage the built-in server for development with manage.py


#### Start the server
```
$ python3 manage.py runserver
```

## Contributors
This project exists thanks to the people who contribute. You're highly encouraged to partipiate in the sites development.

To contribute to the further development of this project, contact the team leads or open an issue. 


### Lead

Lenz Paul [@bringbackthedog]( https://github.com/bringbackthedog )

Matt Williams [@mattcoding4days](https://github.com/mattcoding4days)

### Contributors (in chronological order)

Bohdan Natsevych [@BohdanNatsevych](https://github.com/BohdanNatsevych)

Ezra MacDonald [@macdonaldezra](https://github.com/macdonaldezra)
