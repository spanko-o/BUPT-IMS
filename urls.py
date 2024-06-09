from applications.User.views.user_login_view import UserLoginView
from applications.User.views.user_signup_view import UserSignupView
from applications.home.views.display import HomeAPIView
from applications.home.views.search import SearchAPIView
url_patterns = {
    '/user/signup': UserSignupView,
    '/user/login': UserLoginView,
    '/home/display/page=1': HomeAPIView,
    '/home/search': SearchAPIView
}
