
from app.model import GetContactDetailsModel, SearchByNameModel, SearchByPhoneModel, registerUserModel, spamUserModel




def registerUserControl(data):
    return registerUserModel(data)


def spamUserControl(phone_number, is_spam):
    return spamUserModel(phone_number, is_spam)


def SearchByNameControl(name):
    return SearchByNameModel(name)


def SearchByPhoneControl(name):
    return SearchByPhoneModel(name)


def GetContactDetailsCotrol(phone_number, password):    
    return GetContactDetailsModel(phone_number, password)