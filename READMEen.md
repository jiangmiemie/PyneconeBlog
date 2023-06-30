[Chinese](README.md) | [English](READMEen.md)

## Example

https://www.jiangmiemie.com


## Objective

Build a **easy-to-manage**, **low-coupling**, **free** application website in pure Python (including application demo and documentation instructions) where Markdown is a first-class citizen and the user only needs to place md files to generate web pages.

Reference sites:
[docusaurus](https://docusaurus.io/zh-CN/docs/category/guides)
[pynecone](https://pynecone.io/)

## Use

Default server has Python 3.8 or higher installed

### Preparation
The data uses the default of PGSQL, so you need to **create a new database**. Assume your database information is as follows:

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

### Download the dependencies

`pip install -r requirements.txt`


### Domain name

Apply the front-end domain and back-end domain and configure SSL.

Modify [constants.py](blog/constants.py)
`MAIN_URL` for your front-end domain name: the front-end is displayed here.
`BACKEND_URL` is your backend domain name: backend services run here, not configured correctly will cause response event exceptions.

### Run

Switch to the directory where this folder is located and run `bash run.sh`