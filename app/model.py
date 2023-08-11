
from app import db, ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flask_bcrypt import Bcrypt
# from bcrypt import check_password_hash


class User_profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120), nullable=False)
    is_spam = db.Column(db.Boolean, nullable=False, default=False)  
    

class User_profileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User_profile
        exclude = ('password',)


# This model for user registration
def registerUserModel(user_data):
    try:
        name = user_data.get('name')
        phone_number = user_data.get('phone_number')
        email = user_data.get('email')
        password = user_data.get('password')

        password_hash = Bcrypt().generate_password_hash(password).decode("utf-8")
        if User_profile.query.filter_by(phone_number=phone_number).first():
            return {'Unsuccessful': 'Phone number already registered.'}, 409

        new_user = User_profile(name=name, phone_number=phone_number, email=email if email else None, password=password_hash, is_spam=False)
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User registered successfully.'}, 201

    except Exception as e:
        return {"Unsuccessful": "Server is not responding", 'Error': str(e)}, 500
    finally:
        db.session.close()


# This model for marking a number as spam
def spamUserModel(phone_number, is_spam):
    try:
        is_spam = is_spam.lower() == 'true'
        spam_entry = User_profile.query.filter_by(phone_number=phone_number).first()
        if spam_entry:
            spam_entry.is_spam = is_spam
        else:
            print(spam_entry, "spam_entry")
            spam_entry = User_profile(phone_number=phone_number, is_spam=is_spam)
            db.session.add(spam_entry)
        db.session.commit()
        return {'message': 'Spam number marked successfully.'}, 200
    except Exception as e:
        return {"Unsuccessful": "Server is not responding", 'Error': str(e)}, 500
    finally:
        db.session.close()


# This model for searching the data by name.
def SearchByNameModel(name):
    try:
        results = User_profile.query.filter(User_profile.name.ilike(f'{name}%')).all()
        if not results:
            results = User_profile.query.filter(User_profile.name.ilike(f'%{name}%')).all()
        user_profile_schema = User_profileSchema(many=True).dump(results)
        return {'results': user_profile_schema}, 200    
    except Exception:
        return {"Unsuccessful": "Server is not responding"}, 500
    finally:
        db.session.close()


# This model for searching the data by phone number.
def SearchByPhoneModel(phone_number):
    try:
        results = User_profile.query.filter(User_profile.phone_number.ilike(f'{phone_number}%')).all()
        if not results:
            results = User_profile.query.filter(User_profile.phone_number.ilike(f'%{phone_number}%')).all()        
        user_profile_schema = User_profileSchema(many=True).dump(results)
        return {'results': user_profile_schema}, 200

    except Exception as e:
        return {"Unsuccessful": "Server is not responding"}, 500
    finally:
        db.session.close()


def GetContactDetailsModel(phone_number, password):
    try:
        verify_data = User_profile.query.filter_by(phone_number=phone_number).first()

        if not verify_data:
            return {"Unsuccessful": "Data not Found"}, 404

        if Bcrypt().check_password_hash(verify_data.password, password):
            results = User_profile.query.all()
            if not results:
                return {"Unsuccessful": "Data not Found"}, 404
            user_profile_schema = User_profileSchema(many=True).dump(results)
            return {'results': user_profile_schema}, 200

        return {"Unsuccessful": "Invalid password"}, 401

    except Exception as e:
        return {"Unsuccessful": "Server is not responding"}, 500
    finally:
        db.session.close()