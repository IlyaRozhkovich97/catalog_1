from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import HomePageView, ContactInformationView, ProductListView, ProductDetailView, ProductCreateView, \
    ProductUpdateView, ProductDeleteView
from . import views

app_name = CatalogConfig.name

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('contact/', views.ContactInformationView.as_view(), name='contact'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='specific_product'),
    path('product/new/', views.ProductCreateView.as_view(), name='product_create'),
    path('product/edit/<int:pk>/', views.ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', views.ProductDeleteView.as_view(), name='product_delete'),
]
