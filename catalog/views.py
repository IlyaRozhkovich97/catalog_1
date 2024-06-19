from django.http import HttpResponseRedirect, HttpResponseForbidden
from .forms import ProductForm, VersionFormSet
import csv
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from pytils.translit import slugify
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from catalog.models import Product, Version
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from django.views import View

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
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user  # Добавление пользователя в контекст
        for product in context['products']:
            current_version = Version.objects.filter(product=product, is_current=True).first()
            if current_version:
                product.current_version = current_version
        return context


class ProductDetailView(DetailView):
    model = Product

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:products')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['versions'] = VersionFormSet(self.request.POST)
        else:
            data['versions'] = VersionFormSet()
        data['user'] = self.request.user
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        versions = context['versions']
        if form.is_valid() and versions.is_valid():
            self.object = form.save(commit=False)
            self.object.owner = self.request.user
            self.object.save()
            versions.instance = self.object
            versions.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')

        if not request.user.has_perm('catalog.add_product'):
            return HttpResponseForbidden("У вас нет прав для создания этого продукта.")

        return super().dispatch(request, *args, **kwargs)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:products')
    permission_required = ('catalog.can_edit_product_description', 'catalog.can_edit_product_category')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')

        if not (request.user.has_perm('catalog.can_edit_product_description') and
                request.user.has_perm('catalog.can_edit_product_category')):
            return HttpResponseForbidden("У вас нет прав для редактирования этого продукта.")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['versions'] = VersionFormSet(self.request.POST, instance=self.object)
        else:
            data['versions'] = VersionFormSet(instance=self.object)
        data['user'] = self.request.user
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        versions = context['versions']
        if form.is_valid() and versions.is_valid():
            self.object = form.save(commit=False)
            self.object.slug = slugify(self.object.name)
            self.object.save()
            versions.instance = self.object
            versions.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('catalog:specific_product', args=[self.kwargs['pk']])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:products')

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, 'Продукт успешно удален.')
        return response


class VersionDeleteView(LoginRequiredMixin, DeleteView):
    model = Version
    template_name = 'catalog/version_confirm_delete.html'
    success_url = reverse_lazy('catalog:products')

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, 'Версия успешно удалена.')
        return response


def unpublish_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if not request.user.has_perm('catalog.can_unpublish_product'):
        return HttpResponseForbidden("У вас нет прав для отмены публикации продукта.")

    product.is_published = False
    product.save()
    messages.success(request, 'Продукт успешно снят с публикации.')
    return redirect('catalog:products')


@login_required
@permission_required('catalog.change_product', raise_exception=True)
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form})


def unpublish_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if not request.user.has_perm('catalog.can_unpublish_product'):
        return HttpResponseForbidden("У вас нет прав для отмены публикации этого продукта.")

    product.is_published = False
    product.save()
    messages.success(request, 'Продукт успешно снят с публикации.')
    return redirect('catalog:products')