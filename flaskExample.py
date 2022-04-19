from urllib import response
from flask import Flask,request
from flask_classful import FlaskView,route
from flask import jsonify


app = Flask(__name__)
class TestView(FlaskView):
    route_base = '/'

    def index(self):
    # http://localhost:5000/
        return jsonify({})

    @route('/second')
    def second(self,methods=['POST']):
    # http://localhost:5000/second
        print(request.get_json())
        response = jsonify({'status':'success','method':'second'})
        return response,200
    
    @route('/third/<name>', methods=['POST'])
    def third(self,name):
    # http://localhost:5000/third/yourname
        response = jsonify({'status':'success','method':'third','name':name})
        return response,200

TestView.register(app,route_base = '/')
app.run()