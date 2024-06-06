from applications.User.views.user_login_view import UserLoginView
from applications.User.views.user_signup_view import UserSignupView

url_patterns = {
    '/user/signup': UserSignupView,
    '/user/login': UserLoginView,

}
