from django.conf.urls import url
from planner import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^index$', views.index, name='index'),
        url(r'^about/$', views.about, name='about'),
        url(r'^project/(?P<project_name_slug>[\w\-]+)/$', views.project, name='project'),
        url(r'^add_project/$', views.add_project, name='add_project'), 
        url(r'^project/(?P<project_name>[\w\-]+)/(?P<feature_pk>\d+)/$', views.feature, name='feature'),
        url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
        url(r'^register/$', views.register, name='register'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^restricted/', views.restricted, name='restricted'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^goto/$', views.track_url, name='goto'),
        url(r'^profile/$', views.profile, name='profile'),
        url(r'^like_project/$', views.like_project, name='like_project'),
        url(r'^suggest_category/$', views.suggest_category, name='suggest_category'),
        url(r'^auto_add_page/$', views.auto_add_page, name='auto_add_page'),
        url(r'^project/(?P<project_name>[\w\-]+)/review/$', views.review, name='review'),        
        url(r'^tree_node_content/$', views.get_tree_node_content, name='tree_node_content'),        
        ]
