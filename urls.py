from applications.User.views.user_login_view import UserLoginView
from applications.User.views.user_signup_view import UserSignupView

from applications.Admin.views.admin_signup_view import AdminSignupView

url_patterns = {
    # User
    '/user/signup': UserSignupView,
    '/user/login': UserLoginView,

    # Admin
    '/admin/signup': AdminSignupView,
}
