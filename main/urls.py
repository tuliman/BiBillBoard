from django.urls import path
from .views import index, other_page, BBLoginView, profile, BBLogoutView, ChangeUserInfoView, BBPasswordChangeView, \
    RegisterUserView, RegisterDoneView, user_activate

app_name = 'main'

urlpatterns = [
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index'),
    path('acount/register/activate/<str:sign>/', user_activate, name="register_activate"),
    path('acount/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('acount/register/', RegisterUserView.as_view(), name='register'),
    path('acount/login/', BBLoginView.as_view(), name='login'),
    path('acount/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('acount/profile/', profile, name='profile'),
    path('acount/logout/', BBLogoutView.as_view(), name='logout'),
    path('acount/password/change/', BBPasswordChangeView.as_view(), name='password_change'),
]
