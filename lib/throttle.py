from rest_framework.throttling import UserRateThrottle


class LoginThrottle1(UserRateThrottle):
    scope = 'otp1'
    rate = '2/m'


class LoginThrottle2(UserRateThrottle):
    scope = 'otp2'
    rate = '10/d'
