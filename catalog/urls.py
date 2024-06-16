from django.urls import path
from catalog.apps import CatalogConfig
from . import views

app_name = CatalogConfig.name

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('contact/', views.ContactInformationView.as_view(), name='contact'),  # страница контакты
    path('products/', views.ProductListView.as_view(), name='products'),  # страница продукты
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='specific_product'),  # просмотр продукта
    path('product/new/', views.ProductCreateView.as_view(), name='product_create'),  # cоздание продукта
    path('product/edit/<int:pk>/', views.ProductUpdateView.as_view(), name='product_update'),  # редактирование продукта
    path('product/delete/<int:pk>/', views.ProductDeleteView.as_view(), name='product_delete'),  # удаление продукта
    path('product/<int:product_id>/version/<int:pk>/delete/', views.VersionDeleteView.as_view(), name='version_delete'),
]
