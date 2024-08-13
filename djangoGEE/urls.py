"""djangoGEE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from gee import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    # path('',views.Home.as_view(), name="home"),
    path('admin/', admin.site.urls),
    path('',views.index, name="index"),
    path('home/',views.home, name="home"),
    path('map/',views.map, name="map"),
    path('generate-ndvi-map/', views.generate_ndvi_map, name='generate_ndvi_map'),
    path('chart/', views.generate_chart, name='generate_chart'),
    path('gee/', views.GEE, name='gee'),
    path('result_options/', views.result_options, name="result_options"),
    path('result_options/temp_result/', views.temp_result, name = "temp_results" ),
    path('api/chart-data/', views.chart, name='chart_data_api'),
 









    #Auth
    path('login/',auth_views.LoginView.as_view(template_name = 'login.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(), name='logout'),
    path("signup/",views.signup, name ='signup'),
    path('settings/change_password/', auth_views.PasswordChangeView.as_view(template_name='change_password.html'),name='password_change'),
    path('settings/change_password/done',auth_views.PasswordChangeDoneView.as_view(template_name='change_password_done.html'),name='password_change_done'),
    path('account/', views.UserUpdateView.as_view(), name = 'my_account'),

]















    # path('export_image/', views.export_image_to_drive, name='export_image_to_drive'),