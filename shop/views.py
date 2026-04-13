from django.shortcuts import render
from .models import Product, Order, OrderItem
from django.shortcuts import redirect #tạo function giỏ hàng

def home(request):
    products = Product.objects.all()
    return render(request, 'shop/index.html', {'products': products})

#tạo trang chi tiết sản phẩm
def product_detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'shop/detail.html', {'product': product})

#tạo function giỏ hàng
def add_to_cart(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        cart[str(id)] += 1
    else:
        cart[str(id)] = 1

    request.session['cart'] = cart
    return redirect('/cart/')

#hiển thị giỏ hàng
def view_cart(request):
    cart = request.session.get('cart', {})
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
        'total': total
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

        for id, qty in cart.items():
            product = Product.objects.get(id=id)

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=qty
            )

        # Xóa giỏ hàng
        request.session['cart'] = {}

        return redirect('/')

    return redirect('/')