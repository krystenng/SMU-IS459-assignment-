from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('post/ajax/post', views.uploadPost, name = 'upload_post'),
    path('post-count-chart', views.get_kafka_posts, name = 'post-count-chart'),
    path('barchart', views.get_barchart, name = 'get-bar-chart'),
    path('kafka', views.get_kafka_posts, name = 'get_kafka_posts'),
]
