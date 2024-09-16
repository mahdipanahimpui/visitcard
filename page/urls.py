from django.urls import path
from .import views

app_name = 'page'
urlpatterns = [
    # path('', views.HomeView.as_view(), name='home_view'),

    path('create/', views.PageCreateView.as_view()),
    path('', views.PageListView.as_view()),
    path('retrieve/<int:pk>/', views.PageRetrieveView.as_view()),
    path('update/<int:pk>/', views.PageUpdateView.as_view()),
    path('destroy/<int:pk>/', views.PageDestroyView.as_view()),

    path('<int:page_id>/images/', views.ImageCreateListView.as_view()),
    path('<int:page_id>/images/<int:image_id>', views.ImageRetrieveUpdateDestroyView.as_view()),

    path('<int:page_id>/comminucations/', views.ComminucationCreateListView.as_view()),
    path('<int:page_id>/comminucations/<int:comminucation_id>', views.ComminucationRetrieveUpdateDestroyView.as_view()),

    path('<int:page_id>/locations/', views.LocationCreateListView.as_view()),
    path('<int:page_id>/locations/<int:location_id>', views.LocationRetrieveUpdateDestroyView.as_view()),

    path('<int:page_id>/addresses/', views.AddressCreateListView.as_view()),
    path('<int:page_id>/addresses/<int:address_id>', views.AddressRetrieveUpdateDestroyView.as_view()),

]



