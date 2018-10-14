from django.conf.urls import url

from App import views,shuju1

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/', views.home, name='home'),
    url(r'^register/', views.user_register, name='register'),
    url(r'^login1/', views.user_login1, name='login1'),
    url(r'^login2/', views.user_login2, name='login2'),
    url(r'^fenxi/', shuju1.fenxi, name='fenxi'),

]