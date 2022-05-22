from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import JsonResponse
from .forms import LoginUserForm, RegisterUserForm
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
import json
import datetime
from django.views.generic import CreateView
from .models import Products, Category, Gender, Colors, Types, Order, OrderItem, ShippingAddress


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = data['form']['total']
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                country=data['shipping']['country'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    else:
        print('User not logged in... ')
    return JsonResponse('Payment complete successfully!', safe=False)


def deleteItem(request, productId):
    customer = request.user
    product = Products.objects.get(pk=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    orderItem.delete()


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user
    product = Products.objects.get(pk=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    else:
        orderItem.quantity = 0

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {
            'get_cart_total': 0,
            'get_cart_item': 0,
            'shipping': False,
        }
    context = {
        'items': items,
        'order': order,
    }
    return render(request, 'main/checkout.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {
            'get_cart_total': 0,
            'get_cart_item': 0,
            'shipping': False,
        }
    context = {
        'items': items,
        'order': order,
    }
    return render(request, 'main/cart.html', context)


def view(request, product_id):
    products = Products.objects.filter(pk=product_id)

    context = {
        'products': products,
    }
    return render(request, 'main/index.html', context=context)


def search(request):
    searched = request.GET.get('search')
    cats = Category.objects.all()
    types = Types.objects.all()
    genders = Gender.objects.all()
    colors = Colors.objects.all()
    products = Products.objects.all().filter(product_description__contains=searched)

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


def index(request):
    products = Products.objects.all()
    cats = Category.objects.all()
    types = Types.objects.all()
    genders = Gender.objects.all()
    colors = Colors.objects.all()
    staff = User.objects.filter(is_staff=False)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {
            'get_cart_total': 0,
            'get_cart_item': 0,
            'shipping': False,
        }
        cartItems = 0

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
        'items': items,
        'order': order,
        'cartItems': cartItems,
        'staff': staff,
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


def userProfile(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {
            'get_cart_total': 0,
            'get_cart_item': 0,
            'shipping': False,
        }
    context = {
        'items': items,
        'order': order,
        'user': request.user,
        'fullname': request.user.get_full_name()
    }

    return render(request, 'main/userProfile.html', context)
