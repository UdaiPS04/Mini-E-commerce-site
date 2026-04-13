from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

def home(request):
    products = Product.objects.all()[:3]

    min_price = request.GET.get('min')
    max_price = request.GET.get('max')

    if min_price:
        products = products.filter(price__gte=int(min_price))

    if max_price:
        products = products.filter(price__lte=int(max_price))

    products = products[:3]   # only 3 products

    return render(request, 'home.html', {'products': products})


def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        Contact.objects.create(
            name=name,
            email=email,
            message=message
        )

        return render(request, 'contact.html', {'success': True})

    return render(request, 'contact.html')
from .models import Contact
@login_required(login_url='login')
def queries(request):
    data = Contact.objects.all()
    return render(request, 'queries.html', {'data': data})

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def loginView(request):
    if request.method == 'POST':
        userName = request.POST.get('userName')  
        password = request.POST.get('password')

        user = authenticate(request, username=userName, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, "login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "login.html")

def signupView(request):
    if request.method == "POST":
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        userName = request.POST.get('userName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        if password == cpassword:
            user = User.objects.create_user(
                username=userName,
                email=email,
                password=password
            )
            user.first_name = firstName
            user.last_name = lastName
            user.save()

            return redirect("login")

    return render(request, "signup.html")
def logoutView(request):
    logout(request)
    return redirect('login')

def products(request):
    products = Product.objects.all() 
    return render(request, 'products.html', {'products': products})
def add_to_cart(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        cart[str(id)] += 1
    else:
        cart[str(id)] = 1

    request.session['cart'] = cart

    return redirect('products')
def cart_view(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0

    for key, value in cart.items():
        product = Product.objects.get(id=key)
        product.quantity = value
        product.total_price = product.price * value
        total += product.total_price
        products.append(product)

    return render(request, 'cart.html', {
        'products': products,
        'total': total
    })
def remove_from_cart(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        del cart[str(id)]

    request.session['cart'] = cart
    return redirect('cart')
def increase_qty(request, id):
    cart = request.session.get('cart', {})
    if str(id) in cart:
        cart[str(id)] += 1
    request.session['cart'] = cart
    return redirect('cart')


def decrease_qty(request, id):
    cart = request.session.get('cart', {})
    if str(id) in cart:
        cart[str(id)] -= 1
        if cart[str(id)] <= 0:
            del cart[str(id)]
    request.session['cart'] = cart
    return redirect('cart')
def category_view(request, category):
    products = Product.objects.filter(category=category)
    return render(request, 'products.html', {'products': products})
def new_arrivals(request):
    products = Product.objects.order_by('-created_at')[:2]  # only 2
    return render(request, 'new_arrivals.html', {'products': products})