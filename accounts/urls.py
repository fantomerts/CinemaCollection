from django.urls import path
 
from .views import SignUpView, MyPageView
 
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('settings/',MyPageView.as_view(),name="my-page")
]