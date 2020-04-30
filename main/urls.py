from django.urls import path
from .views import index, other_page, BBLoginView, profile, BBLogoutView, ChangeUserInfoView, BBPasswordChangeView

app_name = 'main'

urlpatterns = [
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index'),
    path('acount/login/', BBLoginView.as_view(), name='login'),
    path('acount/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('acount/profile/', profile, name='profile'),
    path('acount/logout/', BBLogoutView.as_view(), name='logout'),
    path('acount/password/change/', BBPasswordChangeView.as_view(), name='password_change'),
]
