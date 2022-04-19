from urllib import response
from flask import Flask,request
from flask_classful import FlaskView,route
from flask import jsonify


app = Flask(__name__)
class TestView(FlaskView):
    route_base = '/'

    def index(self):
    # http://localhost:5000/
        return jsonify({"hwkk":"dcd"}),200

    @route('/second')
    def secondfn(self,methods=['POST']):
    # http://localhost:5000/second
        print(request.get_json())
        response = jsonify({'status':'success','method':'second',"name":request.get_json()["name"]})
        return response,200
    
    @route('/third/<name>', methods=['POST'])
    def thirdfn(self,name):
    # http://localhost:5000/third/yourname
        response = jsonify({'status':'success','method':'third','name':name})
        return response,200

TestView.register(app,route_base = '/')
app.run()