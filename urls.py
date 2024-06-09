from applications.User.views.user_login_view import UserLoginView
from applications.User.views.user_signup_view import UserSignupView

from applications.Home.views.home_display_view import HomeAPIView
from applications.Home.views.home_search_view import SearchAPIView

from applications.Admin.views.admin_signup_view import AdminSignupView
from applications.Admin.views.info_add_view import NewsAddView

url_patterns = {
    # User
    '/user/signup': UserSignupView,
    '/user/login': UserLoginView,

    # Home
    '/home/display': HomeAPIView,
    '/home/search': SearchAPIView,

    # Admin
    '/admin/signup': AdminSignupView,
    '/admin/add_news': NewsAddView,
}
