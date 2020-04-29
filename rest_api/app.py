from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonpify
from validate_email import validate_email
from datetime import datetime

db_connect = create_engine('sqlite:///../DB/current.db')
db_connect2 = create_engine('sqlite:///../DB/request.db')
app = Flask(__name__)
api = Api(app)

listenerLimit = 50
secretTxt = 'shihabektanoobgamer123890shihabgay#NOOB'

class status(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute("select * from CURRENT") # This line performs query and returns json result
        return {'current': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]} # Fetches first column that is Employee ID

class config(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        email = json_data['email']
        password = json_data['password']
        is_valid = validate_email(email)
        if(is_valid):
            if(password.find('Meow1234ALCHEMIST#1234') > -1):
                return {
                    'secret': secretTxt,
                    'limit':listenerLimit
                }
            
        return 'PAGE DOES NOT EXIST',404

class song_request(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        secret = json_data['secret']
        json_data['secret'] = ''
        if secret == secretTxt:
            name = json_data['name'].replace('"','')
            song = json_data['song'].replace('"','')
            artist = json_data['artist'].replace('"','')
            now = datetime.now()
            timestamp = datetime.timestamp(now)
            path=''
            status = 0

            conn = db_connect2.connect() # connect to database
            query = conn.execute("INSERT INTO REQ (name,song,artist,path,time,status) values('"+name+"','"+song+"','"+artist+"','"+path+"','"+str(timestamp)+"',"+str(status)+");")

            return {
                'status':'request submitted',
                'data': json_data
            }
        return 'PAGE DOES NOT EXIST',404


api.add_resource(status, '/current') # Route_1
api.add_resource(song_request, '/request') # Route_2
api.add_resource(config, '/config') # Route_2

if __name__ == '__main__':
     app.run()