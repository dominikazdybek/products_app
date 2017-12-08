# products_app

*products_app* is an application written during the programming bootcamp course as a final project. The application is used to evaluate products by users.

Application functionalities is:

* user login/registration
* assessment of the product - like/dislike
* adding a comment
* editing/deleting own comment
* browsing products by category
* displaying the best-rated products
* displaying the most frequently commented products

## Stack

* Python
* Django
* MySQL
* REST
* jQuery stack
* HTML + CSS (Bootstrap)

## How to build the project locally

### 1. Download

You need the products_app project files in your workspace:

`$ git clone https://github.com/dominikazdybek/products_app.git`

### 2. Virualenv

Create virtualenv for your project and activate it:

`$ virtualenv -p python3 products_env`

`$ source products_env/bin/activate`

### 3. Requirements

Download and install MySQL database (prefered version is 5.7). You can get it from here: 

* https://dev.mysql.com/downloads

To install all required dependencies, simply type:

`$ cd products_app`

`$ pip install -r requirements.txt`

### 4. How to run?

First, create database called `products` in MySQL. Then define your credentials in settings file: `project/settings.py`.

Make migration:

* `/manage.py migrate`

Run server:

* `/manage.py runserver`


## REST API Documentation
