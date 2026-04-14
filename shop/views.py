from django.shortcuts import render
from .models import Product, Category, Order, OrderItem
from django.shortcuts import redirect #tạo function giỏ hàng
from django.core.mail import send_mail #gửi đơn hàng qua email
from django.conf import settings
from django.contrib import messages

def home(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    products = Product.objects.all()
    categories = Category.objects.all()
    cart = request.session.get('cart', {}) 
    cart_count = sum(cart.values())

    # search
    if query:
        products = products.filter(name__icontains=query)

    # filter category
    if category_id:
        products = products.filter(category_id=category_id)

    return render(request, 'shop/index.html', {
        'products': products,
        'categories': categories,
        'query': query,
        'category_id': category_id,
        'cart_count': cart_count,
    })

#tạo trang chi tiết sản phẩm
def product_detail(request, id):
    product = Product.objects.get(id=id)
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    featured_products = Product.objects.filter(is_featured=True)

    return render(request, 'shop/detail.html', {
        'product': product,
        'featured_products': featured_products,
        'cart_count': cart_count,
    })

#tạo function giỏ hàng
def add_to_cart(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        cart[str(id)] += 1
    else:
        cart[str(id)] = 1

    request.session['cart'] = cart

    # THÔNG BÁO
    messages.success(request, "✅ Đã thêm vào giỏ hàng!")

    return redirect('/')

#hiển thị giỏ hàng
def view_cart(request):
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())

    products = []
    total = 0

    for id, qty in cart.items():
        product = Product.objects.get(id=id)
        product.qty = qty
        product.total = product.price * qty
        total += product.total
        products.append(product)

    return render(request, 'shop/cart.html', {
        'products': products,
        'total': total,
        'cart_count': cart_count
    })

#Xử lý đặt hàng
def checkout(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        order = Order.objects.create(
            name=name,
            phone=phone,
            address=address
        )

        cart = request.session.get('cart', {})

        message = f"Khách: {name}\nSĐT: {phone}\nĐịa chỉ: {address}\n\nĐơn hàng:\n"

        for id, qty in cart.items():
            product = Product.objects.get(id=id)

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=qty
            )

            message += f"- {product.name} x {qty}\n"

        # GỬI EMAIL
        send_mail(
            'Đơn hàng mới từ website',
            message,
            settings.EMAIL_HOST_USER,   # chuẩn hơn
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        # Xóa giỏ hàng
        request.session['cart'] = {}

        return redirect('/')

    return redirect('/')

#Tăng giảm sp trong giỏ hàng
def update_cart(request, id, action):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        if action == 'increase':
            cart[str(id)] += 1
        elif action == 'decrease':
            cart[str(id)] -= 1

            if cart[str(id)] <= 0:
                del cart[str(id)]

    request.session['cart'] = cart
    return redirect('/cart/')


def remove_from_cart(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        del cart[str(id)]

    request.session['cart'] = cart
    return redirect('/cart/')