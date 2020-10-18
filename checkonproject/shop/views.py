from django.shortcuts import render
from .models import Product, Category
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Cart, Order
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import F
# from django.db.models import Avg, Max, Min, Sum, Count

# Create your views here.

def index(request):
    return render(request, 'index.html')

def show_category(request, category_id):
    categories = Category.objects.all()
    category = Category.objects.get(pk=category_id)
    products = Product.objects.filter(category=category).order_by('pub_date')
    lank_products = Product.objects.filter(category=category).order_by('-hit')[:4]
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    return render(request, 'shopping.html', {'category': category, 'categories': categories ,'posts' : posts})

def cart(request, user_id):
    categories = Category.objects.all()
    user = User.objects.get(pk=user_id)
    cart = Cart.objects.filter(user=user)
    print(user)
    paginator = Paginator(cart, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    total_prices = 0
    for i in cart:
        print(i)
        i.products.price = i.products.price * i.quantity
        total_prices = total_prices + i.products.price    
    cart.totalAmount = total_prices
    print(cart.totalAmount)
    

    # 카테고리별 산 상품 종류 합계
    isBought = {}
    print(type(isBought))
    for i in cart:
        if i.category_id in isBought:
            sum = isBought.get(i.category_id) + 1
            isBought[i.category_id] = sum
        else:
            isBought[i.category_id] = 1

    # 구매 제품 종류 합계
    totalSum=0
    for key, value in isBought.items():
        totalSum = totalSum + value
        print(key, " : ", value)

    # 카테고리 통계
    countProduct = {}
    for i in cart:
        countProduct[i.category_id] = isBought.get(i.category_id) / totalSum * 100

    for key, value in countProduct.items():
        print(key, " : ", value)

    context = {'user': user, 'cart': cart, 'categories': categories, 'posts' : posts, 'countProduct' : countProduct}

    return render(request, 'cart.html', context)

def mypage(request, user_id):
    categories = Category.objects.all()
    user = User.objects.get(pk=user_id)
    cart = Cart.objects.filter(user=user)
    print(user)
    paginator = Paginator(cart, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    total_prices = 0
    for i in cart:
        print(i)
        i.products.price = i.products.price * i.quantity
        total_prices = total_prices + i.products.price    
    cart.totalAmount = total_prices
    print(cart.totalAmount)
    

    # 카테고리별 산 상품 종류 합계
    isBought = {}
    print(type(isBought))
    for i in cart:
        if i.category_id in isBought:
            sum = isBought.get(i.category_id) + 1
            isBought[i.category_id] = sum
        else:
            isBought[i.category_id] = 1

    # 구매 제품 종류 합계
    totalSum=0
    for key, value in isBought.items():
        totalSum = totalSum + value
        print(key, " : ", value)

    # 카테고리 통계
    countProduct = {}
    for i in cart:
        countProduct[i.category_id] = isBought.get(i.category_id) / totalSum * 100

    for key, value in countProduct.items():
        print(key, " : ", value)

    context = {'user': user, 'cart': cart, 'categories': categories, 'posts' : posts, 'countProduct' : countProduct}

    return render(request, 'mypage.html', context)


def delete_cart(request, product_id):
    user = request.user
    cart = Cart.objects.filter(user=user)
    quantity = 0

    if request.method == 'POST':
        pk = int(request.POST.get('product'))
        product = Product.objects.get(pk=pk)
        for i in cart:
            if i.products == product :
                quantity =  i.quantity
        if quantity > 0 :
            product = Product.objects.filter(pk=pk)
            cart = Cart.objects.filter(user=user, products__in=product)
            cart.delete()
            return redirect('cart', user.pk)

@login_required
def cart_or_buy(request, product_id):
    quantity = request.POST.get('quantity', '')
    product = Product.objects.get(pk=product_id)
    user = request.user
    categories = Category.objects.all()
    category = product.category
    initial = {'name': product.name, 'amount': product.price, 'quantity': quantity, 'category':product.category}
    cart = Cart.objects.filter(user=user)
    if request.method == 'POST':
        if 'add_cart' in request.POST:
            for i in cart :
                if i.products == product:
                    product = Product.objects.filter(pk=product_id)
                    Cart.objects.filter(user=user, products__in=product).update(quantity=F('quantity') + quantity)
                    messages.success(request,'장바구니 등록 완료')
                    return redirect('shopping', category.pk)
            Cart.objects.create(user=user, products=product, quantity=quantity, category=category)
            return redirect('shopping', category.pk)

