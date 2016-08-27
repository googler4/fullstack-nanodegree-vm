from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask.ext.pymongo import PyMongo
import json
from bson import json_util
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
from database_setup import Base, Restaurant, MenuItem

mongo = MongoClient("mongodb://lva1-learnin01/:27019")
db = mongo.learninDev
collection = db.analytics

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/hello')
def HelloWorld():
    return "Hello World"

@app.route('/xapi')
def xapi():
	
	cursor = collection.find().limit(1);
	json_docs = [json.dumps(doc, default=json_util.default) for doc in cursor]
	docs = [json.loads(j_doc, object_hook=json_util.object_hook) for j_doc in json_docs]
   	print(json_docs)
	

	return render_template('render.html', user=json_docs)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)