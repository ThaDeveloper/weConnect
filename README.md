# weConnect

[![Build Status](https://travis-ci.org/ThaDeveloper/weConnect.svg?branch=challenge2)](https://travis-ci.org/ThaDeveloper/weConnect)
[![Coverage Status](https://coveralls.io/repos/github/ThaDeveloper/weConnect/badge.svg?branch=challenge2)](https://coveralls.io/github/ThaDeveloper/weConnect?branch=challenge2)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/cfc7addc7b1b4fbc90574ab6f4192dde)](https://www.codacy.com/app/ThaDeveloper/weConnect?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ThaDeveloper/weConnect&amp;utm_campaign=Badge_Grade)

A platform that provides a platform that brings businesses and individuals together.

weConnect brings people close to their favorites businesses all across the globe.

## What can users do?

1. Create an account
2. Register a business
3. Update their business details
4. Delete their business
5. View available business and provide reviews
6. Search for other businesses based on name, location or category.

##  Run the UI

`$git clone https://github.com/ThaDeveloper/weConnect.git`

Ensure you have bootstrap 3.3.7 or later.( Can download or use available CDNs.Remember to link jquery as the UI animations rely on javascipt/jquery). Find more [here](http://getbootstrap.com)

`$ cd weConnect` and open the index.html file

## Inside the platform

### Login Page 

![alt text](https://github.com/ThaDeveloper/weConnect/blob/challenge1/designs/documentation/snapshots/login.png "Login Page")

### Dashboard Page

![alt text](https://github.com/ThaDeveloper/weConnect/blob/challenge1/designs/documentation/snapshots/dashboard.png "User Registration page")

### Add Business Page

![alt text](https://github.com/ThaDeveloper/weConnect/blob/challenge1/designs/documentation/snapshots/add_business.png "Add business page")


### Business Profile Page

![alt text](https://github.com/ThaDeveloper/weConnect/blob/challenge1/designs/documentation/snapshots/business.png "Dashboard")


### Reviews Page

![alt text](https://github.com/ThaDeveloper/weConnect/blob/challenge1/designs/documentation/snapshots/reviews.png "Business profile page")

### Mobile version

![alt text](https://github.com/ThaDeveloper/weConnect/blob/challenge1/designs/documentation/snapshots/mobile_version.png "Mobile version")
bile_version.png "Mobile version")


## Run the API
### What you need
- python 3.5 or later
- A working Virtual environment

### Installation
1. Create a [virtual environment](http://www.pythonforbeginners.com/basics/how-to-use-python-virtualenv)
`$ virtualenv envname` and then `$ source envname/bin/activate`
On the weConnect directory

2. Install project dependencies
`$ pip install -r requirements.txt`

Finally run `$ python3 views.py`

### Testing
Run command 
`$ nosetests tests --with-coverage --cover-package=src`

### API Endpoints
#### To note
- User needs to be logged in to: Register, update or remove business and also to give reviews
1. Users 
- `POST /api/v1/auth/register` Creates user account
- `POST /api/v1/auth/login` Log in user
- `POST /api/v1/auth/logout` Logout user
- `PUT /api/v1/auth/reset-password` Resets user password
2. Businesses
- `POST /api/v1/businesses` Register new business
- `GET /api/v1/businesses` List all available businesses
- `PUT /api/v1/businesses/<business_id>` Update business 
- `DELETE /api/v1/businesses/<business_id>` Remove business
3. Reviews
- `POST /api/v1/businesses/<business_id>/reviews` Review a business
- `GET /api/v1/businesses/<business_id>/reviews` Get business' reviews


## Credits
[Justin Ndwiga](https://github.com/ThaDeveloper)

## License

MIT License

Copyright (c) 2018 Justin Ndwiga

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

```THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.```


