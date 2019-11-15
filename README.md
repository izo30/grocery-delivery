# Grocery Delivery

[![Build Status](https://travis-ci.com/izo30/grocery-delivery.svg?token=TBAvqzqhSSPTjTBPv1sK&branch=develop)](https://travis-ci.com/izo30/grocery-delivery)

An API for a grocery ecommerce app

## Available Endpoints:

| Http Method | Endpoint Route | Endpoint Functionality
| --- | --- | --- |
| `POST` | /api/customers/account | Signup new customer |
| `POST` | /api/customers/login | Login a customer |
| `PATCH` | /api/customers/account | Edit customer details |
| `DELETE` | /api/customers/account | Delete a customer |
| `POST` | /api/admin | Create new admin |
| `POST` | /api/admin/login | Login an admin |
| `PATCH` | /api/admin | Edit an admin |
| `DELETE` | /api/admin | Delete an admin |
| `POST` | /api/categories | Create a category |
| `GET` | /api/categories | Get all categories |
| `DELETE` | /api/categories | Delete a category |
| `POST` | /api/groceries | Create a grocery |
| `GET` | /api/groceries | Get all groceries |
| `PATCH` | /api/groceries | Edit a grocery |
| `GET` | /api/groceries/category/{category_id} | Get groceries for a category |
| `DELETE` | /api/groceries/{grocery_id} | Delete a grocery |
| `GET` | /api/groceries/{grocery_id} | Get a grocery |

## Prerequisites

```
- pip
- virtualenv
- python 3
```

## Installation
Clone the repo
```
git clone https://github.com/izo30/grocery-delivery
```
Create a virtual environment
```
virtualenv <environment name>
```
Activate the environment
```
$source <your environment name>/bin/activate
```
Install dependencies
```
$pip install -r requirements.txt
```
Run the app
```
python run.py
```

## Deployment
The api is deployed on heroku on [THIS](https://grocery-delivery.herokuapp.com/api/ "Heroku Link") link

## Built with
Flask, a python framework

## Authors
[Isaac Wangethi](https://github.com/izo30 "Isaac Wangethi")