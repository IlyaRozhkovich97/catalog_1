from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import HomePageView, ContactInformationView, ProductListView, ProductDetailView, ProductCreateView, \
    ProductUpdateView, ProductDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='specific_product'),
    path('home/', HomePageView.as_view(), name='home'),
    path('contacts/', ContactInformationView.as_view(), name='contact'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
]
