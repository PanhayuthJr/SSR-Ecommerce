from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm, CategoryForm

def store(request):
    # Get cart data (works for logged-in or guest users)
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    # Handle authenticated user safely
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user)
        product = Product.objects.get(id=productId)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

        if action == 'add':
            orderItem.quantity += 1
        elif action == 'remove':
            orderItem.quantity -= 1

        orderItem.save()

        if orderItem.quantity <= 0:
            orderItem.delete()
    else:
        # For guest users, handle cart in cookies
        cart = cookieCart(request)
        if action == 'add':
            cart[productId] = cart.get(productId, 0) + 1
        elif action == 'remove':
            if cart.get(productId, 0) > 1:
                cart[productId] -= 1
            else:
                cart.pop(productId, None)

        # Save updated cart to cookie
        response = JsonResponse('Item was added', safe=False)
        response.set_cookie('cart', json.dumps(cart))
        return response

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    # Save shipping info if needed
    if order.shipping:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Create User
            # Create associated Customer
            Customer.objects.create(
                user=user,
                name=user.username,
                email=user.email
            )
            messages.success(request, 'Your account has been created successfully! Please login.')
            return redirect('login')  # redirect to login page
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})


def logoutUser(request):
    logout(request)
    return redirect('store')  # redirect to homepage after logout

# ---------------- Category CRUD ----------------
@login_required(login_url='login')
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'store/category_list.html', {'categories': categories})


@login_required(login_url='login')
def category_create(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('category_list')
    return render(request, 'store/category_form.html', {'form': form})


@login_required(login_url='login')
def category_update(request, pk):
    category = get_object_or_404(Category, id=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('category_list')
    return render(request, 'store/category_form.html', {'form': form})


@login_required(login_url='login')
def category_delete(request, pk):
    category = get_object_or_404(Category, id=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'store/category_confirm_delete.html', {'category': category})


# ---------------- Product CRUD ----------------
@login_required(login_url='login')
def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})


@login_required(login_url='login')
def product_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'store/product_form.html', {'form': form})


@login_required(login_url='login')
def product_update(request, pk):
    product = get_object_or_404(Product, id=pk)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'store/product_form.html', {'form': form})


@login_required(login_url='login')
def product_delete(request, pk):
    product = get_object_or_404(Product, id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'store/product_confirm_delete.html', {'product': product})