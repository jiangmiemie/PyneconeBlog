[Chinese](README.md) | [English](READMEen.md)

## Objectives

Build a **easy to manage**, **low coupling**, **free** application website in pure Python


## Use

Default server with Python 3.8 or higher installed

### Preparation
The database uses PGSQL, so you need to **create a new database**. Assume your database information is as follows:

database=reflexblog
user=reflexblog
password=yourpassword

Then, please create a new `database.ini` file in the root directory with the following content:

```
[postgresql]
host=localhost
database=reflexblog
user=reflexblog
password=yourpassword
```

If you want to use some applications, then please also create a new file `.env` in the root directory and place the relevant apikeys in it. For example

```
OPENAIKEY = "sk-****************************"
```

### Download the dependencies

``pip install -r requirements.txt``


### Domain name

Apply the front-end domain and back-end domain, and configure SSL.

Modify [constants.py](blog/constants.py)
`MAIN_URL` for your front-end domain name: the front-end is displayed here.
`BACKEND_URL` is your backend domain name: backend services run here, not configured correctly will cause response event exceptions.

### Run

Switch to the directory where this folder is located (/web) and run `bash run.sh`