from django.urls import path
from . import views
from .views import Register_Users

urlpatterns = [
    path('', views.apiOverview, name="api-overview"),
    path('register/', views.Register_Users, name='auth_register'),
    path('login/', views.login_user, name='auth_login'),
    path('logout/', views.User_logout, name='auth_logout'),
    path('accdelete/', views.Acc_delete, name='acc_delete'),
    path('edituser/', views.Edit_User, name='edit_user'),
    path('userincomingrequest/', views.userincomingrequest, name='userincomingrequest'),
    path('useroutgoingrequest/', views.useroutgoingrequest, name='useroutgoingrequest'),
    path('sendrequest/<int:id>/', views.sendrequest, name='sendrequest'),
    path('AccepetRejectRequest/', views.AccepetRejectRequest, name='AccepetRejectRequest'),
]