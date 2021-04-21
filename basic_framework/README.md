# Basic framework

###### Architecture diagram:

![diagram](/basic_framework_diagram.png)

###### Goal:
Our goal is to Send updates from the flask app to the browser.

###### How to run:

* create new virtual environment

* install dependencies: `pip install -r requirements.txt`

* Run locally:
  * Run the server: `uwsgi --ini uwsgi.ini`

* Or run with docker:

`docker build -t simple_example .`

`docker run -p 8888:8888 simple_example`

###### Usage:

* open http://localhost:8888/ on any client

* send an api call to http://localhost:8888/ on any client. 
  For example: http://localhost:8888/api?days=3&units=metric&time=2000
