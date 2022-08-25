from django.urls import path
from apps.user.views import RegisterView,ActiveView,LoginView
urlpatterns = [
    # path('register/',views.register,name='register'),
    # path('register_hand/',views.register_hand,name='register_hand')
    path('register/', RegisterView.as_view(), name='register'),
    path('active/<str:token>/', ActiveView.as_view(), name='active'),
    path('login/', LoginView.as_view(), name='login')
]
