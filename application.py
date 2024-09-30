from os import environ as env
import datetime
import mariadb
from pymongo import MongoClient
import json
from flask import Flask, redirect
import logging

app = Flask(__name__)

if __name__ != '__main__':
  gunicorn_logger = logging.getLogger('gunicorn.error')
  app.logger.handlers = gunicorn_logger.handlers
  app.logger.setLevel(gunicorn_logger.level)

# mariadb configs
db_host = env.get('DBHOSTNAME')
db_port_str = env.get('DBPORT')
db_port = int(db_port_str)
db_user = env.get('DBUSERNAME')
db_pswd = env.get('DBUSERPSWD')
db_name = 'test'

#docdb configs
app.config['DOCDB_URI'] = env.get('DOCDB_URI')


@app.route("/")
def index():
  app.logger.debug('calling index path')
  return "Your Flask App Works!"

@app.route("/hello")
def hello():
  return "Hello World!"

@app.route("/other")
def other():
  return "You're viewing the other path!"

@app.route("/reroute")
def reroute():
  app.logger.debug('redirecting')
  return redirect("https://wgupepnwpn.us-west-2.awsapprunner.com/thanks", code=302)

@app.route("/list")
def list():
  app.logger.debug(f"database endpoint: {db_host}")
  return f"confirmed database endpoint: {db_host}"

@app.route("/health")
def health():
  selected_date = datetime.datetime.now()
  return f'HealthCheck performed at: {selected_date}'


############## DB specific route ############## 
@app.route("/database")
def database():

  #Access database
  try: 
    # connection for MariaDB
    db = mariadb.connect(
      host=db_host,
      port=db_port,
      user=db_user,
      password=db_pswd,
      database=db_name
    )
  except mariadb.Error as e: 
    print(f"Error connecting to MariaDB: {e}")

  app.logger.debug('database connection established')

  cursor = db.cursor()

  # execute a SQL statement
  cursor.execute("select * from people")

  # serialize results into JSON
  row_headers=[x[0] for x in cursor.description]
  rv = cursor.fetchall()
  json_data=[]
  for result in rv:
    json_data.append(dict(zip(row_headers,result)))

  if json_data:
    cursor.close()
    db.close()

  # return the results!
  return f'Successfully connected to your database: {json.dumps(json_data)}'


@app.route("/docdb")
def database():
  
  #Access database and connect to doc_db
  doc_db = MongoClient(app.config['DOCDB_URI']).get_databsae()

  if doc_db:
    app.logger.debug(f"database connection established: {app.config['DOCDB_URI']}")
  else:
    app.logger.debug(f"database connection not established: {app.config['DOCDB_URI']}")

  # return the results!
  results = list(doc_db.my_collection.find())
  doc_db.client.close()
  return f'Successfully connected to your database: {results}'



if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8000, debug=False)