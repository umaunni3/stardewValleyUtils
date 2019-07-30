# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
from flask import Flask, render_template, request, jsonify
#from google.cloud import datastore
import datetime
from table_parsing import *


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/')
def root():
    # Store the current access time in Datastore.
    # store_time(datetime.datetime.now())

    # Fetch the most recent 10 access times from Datastore.
    # times = fetch_times(10)
    data = item_search("daffodil")
    loved = data['Loves']
    liked = data['Likes']
    neutral = data['Neutral']

    return render_template('index.html', css_src="style.css", loved_items=loved, liked_items=liked, neutral_items=neutral)


# /* API ENDPOINT: /query
# * Use this API endpoint to query the database for information;
# * specify which information is desired using the body of the request.
# * {
# *   "category": ["name" | "item"],
# *   "query": [ the name of villager, or name of item ]
# * }
@app.route('/query', methods=['POST'])
def db_query():
    query = request.json['query']
    category = request.json['category']

    print("query: {}, category: {}".format(query, category))
    if category == "Villager":
        return jsonify(villager_search(query))
    elif category == "Item":
        return jsonify(item_search(query))
    return jsonify('hello')



# datastore_client = datastore.Client()

def store_time(dt):
    entity = datastore.Entity(key=datastore_client.key('visit'))
    entity.update({
        'timestamp': dt
    })

    datastore_client.put(entity)


def fetch_times(limit):
    query = datastore_client.query(kind='visit')
    query.order = ['-timestamp']

    times = query.fetch(limit=limit)

    return times




if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
