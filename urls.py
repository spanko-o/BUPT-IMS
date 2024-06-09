from applications.User.views.user_login_view import UserLoginView
from applications.User.views.user_signup_view import UserSignupView

from applications.home.views.display import HomeAPIView
from applications.home.views.search import SearchAPIView


from applications.Admin.views.admin_signup_view import AdminSignupView


url_patterns = {
    # User
    '/user/signup': UserSignupView,
    '/user/login': UserLoginView,
    
    # Home
    '/home/display/page=1': HomeAPIView,
    '/home/search': SearchAPIView

    # Admin
    '/admin/signup': AdminSignupView,
}
