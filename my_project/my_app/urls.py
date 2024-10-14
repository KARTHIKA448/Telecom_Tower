from django.urls import path
from .import views

urlpatterns = [
    path('',views.home,name = 'home'),
    path("dashboard/",views.dashboard,name = "dashboard"),
    path('data/',views.data, name = 'data'),
    path('viewdashboard/<int:id>/', views.detailedview, name='viewdashboard'),

]