

from flask import Blueprint, request
from flask_restx import Api, Resource, fields
from app.control import GetContactDetailsCotrol, SearchByNameControl, SearchByPhoneControl, registerUserControl, spamUserControl



# Create a blueprint for your API routes
spamfinder = Blueprint('spamfinder', __name__, url_prefix='/spamfinder')
spamfinder_api = Api(spamfinder, version="1.0",
                     title="spamFinder",
                     description="Manage global database information")
spamfinderns = spamfinder_api.namespace('spamfinder', description='customer organization details')


user_profile_model = spamfinderns.model('user_profile', {
    'id': fields.Integer(required=True),
    'name': fields.String(required=True),
    'phone_number': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})



# Route for user registration
@spamfinderns.route('/register')
class RegisterUser(Resource):
    @spamfinderns.expect(user_profile_model)
    def post(self):
        try:
            data = request.get_json(force=True)           
            if not data.get('name') or not data.get('phone_number') or not data.get('password'):
                return {'Unsuccesfull': 'Enter required fields.'}, 400
            if len(data['phone_number']) != 10:
                return {'Unsuccessful': 'Phone number should be exactly 10 characters long.'}, 400
            return registerUserControl(data)
        except Exception as e:
            return {'Unsuccessful': 'Looks like you missed something', 'Error': str(e)}



@spamfinderns.route('/markAsSpam')
class MarkSpam(Resource):
    @spamfinderns.doc(params={"phone_number": "987654321", 'is_spam': "true or false"})
    def post(self):
        try:
            phone_number = request.args.get('phone_number')
            is_spam = request.args.get('is_spam')
            if phone_number and is_spam:
                return spamUserControl(phone_number, is_spam)
            else:
                return {'Unsuccessful': 'Invalid request data. Both phone_number and is_spam are required.'}, 400
        except Exception as e:
            return {'Unsuccessful': 'Something went wrong. Error: {}'.format(str(e))}, 500



# Route for getting contact details
@spamfinderns.route('/getContactDetails')
class GetContactDetails(Resource):
    @spamfinderns.doc(params={"phone_number": "xxxxxxxxxx", 'password': "password"})
    def get(self):
        try:
            phone_number = request.args.get('phone_number')
            password = request.args.get('password')
            if phone_number and password:
                return GetContactDetailsCotrol(phone_number, password)
            else:
                return {'Unsuccessful': 'Invalid request data. Both phone_number and password are required.'}, 400
        except Exception as e:
            return {'Unsuccessful': 'Something went wrong. Error: {}'.format(str(e))}, 500


# Route for searching by name
@spamfinderns.route('/searchByName')
class SearchByName(Resource):
    @spamfinderns.doc(params={"name": {"description": "Name to search for.", "required": True}})
    def get(self):
        try:
            name = request.args.get('name')
            if name:
                return SearchByNameControl(name)
            else:
                return {'error': 'Name parameter is required.'}, 400
        except Exception as e:
            return {'Unsuccessful': 'Something went wrong. Error: {}'.format(str(e))}, 500



# Route for searching by phone number
@spamfinderns.route('/searchByPhoneNumber')
class SearchByPhone(Resource):
    @spamfinderns.doc(params={"phone_number": {"description": "phone_number to search for.", "required": True}})
    def get(self):
        try:
            phone_number = request.args.get('phone_number')
            if phone_number:
                return SearchByPhoneControl(phone_number)
            else:
                return {'error': 'Phone number parameter is required.'}, 400        
        except Exception as e:
            return {'Unsuccessful': 'Something went wrong. Error: {}'.format(str(e))}, 500


