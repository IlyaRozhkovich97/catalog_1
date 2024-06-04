from django.http import HttpResponseRedirect
from .forms import ProductForm

import csv

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from catalog.models import Product, Version


class HomePageView(TemplateView):
    template_name = 'catalog/home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(is_published=True)
        return context


class ContactInformationView(TemplateView):
    template_name = 'catalog/contact_information.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        print(
            f"\nСообщение из формы обратной связи:\n\033[91mИмя пользователя:\033[0m {name}\n\033[91mЭлектронная почта:"
            f"\033[0m {email}\n\033[91mТелефон:\033[0m {phone}\n\033[91mСообщение:\033[0m {message} ")

        with open('contact_info.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, phone, message])

        return HttpResponseRedirect(self.request.path)


class ProductListView(ListView):
    model = Product

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = context['object_list']
        for product in products:
            product.active_version = Version.objects.filter(product=product, is_current=True).first()
        return context


class ProductDetailView(DetailView):
    model = Product

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:products')

    def form_valid(self, form):
        if form.is_valid():
            new_prod = form.save(commit=False)
            new_prod.slug = slugify(new_prod.name)
            new_prod.save()
        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    fields = ('name', 'category', 'description', 'purchase_price', 'image')
    success_url = reverse_lazy('catalog:products')

    def form_valid(self, form):
        if form.is_valid():
            new_prod = form.save()
            new_prod.slug = slugify(new_prod.name)
            new_prod.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('catalog:specific_product', args=[self.kwargs['pk']])


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:products')
