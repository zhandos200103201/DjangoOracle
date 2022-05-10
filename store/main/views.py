from django.conf import settings
from django.core.mail import send_mail

from .forms import LoginUserForm, RegisterUserForm
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Products, Category, Gender, Colors, Types

menu = [
    {'title': "Категории", },
    {'title': "Типы", },
    {'title': "Цвета", },
    {'title': "Пол", }
]


def searchProduct(request):
    return render(request, 'main/index.html', {})


def index(request):
    products = Products.objects.all()
    cats = Category.objects.all()
    types = Types.objects.all()
    genders = Gender.objects.all()
    colors = Colors.objects.all()

    context = {
        'products': products,
        'cats': cats,
        'types': types,
        'genders': genders,
        'colors': colors,
        'cat_selected': 0,
        'gender_selected': 0,
        'color_selected': 0,
        'type_selected': 0,
    }

    return render(request, 'main/index.html', context=context)


def show_category(request, category_id):
    products = Products.objects.filter(product_category_id=category_id)
    colors = Colors.objects.all()
    cats = Category.objects.all()
    types = Types.objects.all()
    genders = Gender.objects.all()

    context = {
        'products': products,
        'cats': cats,
        'types': types,
        'genders': genders,
        'colors': colors,
        'cat_selected': category_id,
        'gender_selected': 0,
        'color_selected': 0,
        'type_selected': 0,
    }

    return render(request, 'main/index.html', context=context)


def show_gender(request, gender_id):
    products = Products.objects.filter(product_gender_id=gender_id)
    genders = Gender.objects.all()
    cats = Category.objects.all()
    types = Types.objects.all()
    colors = Colors.objects.all()

    context = {
        'products': products,
        'cats': cats,
        'types': types,
        'genders': genders,
        'colors': colors,
        'cat_selected': 0,
        'gender_selected': gender_id,
        'color_selected': 0,
        'type_selected': 0,
    }

    return render(request, 'main/index.html', context=context)


def show_type(request, type_id):
    products = Products.objects.filter(product_type_id=type_id)
    genders = Gender.objects.all()
    cats = Category.objects.all()
    types = Types.objects.all()
    colors = Colors.objects.all()

    context = {
        'products': products,
        'cats': cats,
        'types': types,
        'genders': genders,
        'colors': colors,
        'cat_selected': 0,
        'gender_selected': 0,
        'color_selected': 0,
        'type_selected': type_id,
    }

    return render(request, 'main/index.html', context=context)


def show_color(request, color_id):
    products = Products.objects.filter(product_color_id=color_id)
    colors = Colors.objects.all()
    genders = Gender.objects.all()
    cats = Category.objects.all()
    types = Types.objects.all()

    context = {
        'products': products,
        'cats': cats,
        'types': types,
        'genders': genders,
        'colors': colors,
        'cat_selected': 0,
        'gender_selected': 0,
        'color_selected': color_id,
        'type_selected': 0,
    }

    return render(request, 'main/index.html', context=context)


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        if form.is_valid():
            cd = form.cleaned_data
            subject = "Вы успешно зарегистрировались."
            message = "Мы поздравляем вас, вы успешно зарегистрировались. Мы очень рады уведить вас в наших редах!!!"
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [cd['email']], fail_silently=False)

        return redirect('home')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


def admin(request):
    return None
