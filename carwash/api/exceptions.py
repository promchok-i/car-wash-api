from rest_framework.exceptions import APIException


class Invalidtime(APIException):
    status_code = 400
    default_detail = 'Invalid Time'
    default_code = 'invalid_time'
    
class AlreadyCheckedIn(APIException):
    status_code = 400
    default_detail = 'Already Checked In'
    default_code = 'already_checked_in'
    
class AlreadyCancelled(APIException):
    status_code = 400
    default_detail = 'Already Cancelled'
    default_code = 'already_cancelled'