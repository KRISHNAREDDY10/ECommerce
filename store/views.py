from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import ProductForm
from django.contrib import messages
from django.db import IntegrityError


# Product List - visible to all users
@login_required
def product_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        products = Product.objects.filter(name__icontains=search_query).order_by('name')
    else:
        products = Product.objects.all().order_by('name')

    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'store/product_list.html', {'page_obj': page_obj})


# Adding a product - restricted to Admin and Seller
@login_required
def create_product(request):
    if request.user.is_authenticated and request.user.userprofile.role in ['Admin', 'Seller']:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Product created successfully.')
                return redirect('store:product_list')
        else:
            form = ProductForm()
        return render(request, 'store/product_form.html', {'form': form, 'action': 'Create'})

    messages.error(request, 'You do not have permission to create a product.')
    return redirect('store:product_list')


# Update a product - restricted to Admin and Seller
@login_required
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user.role in ['Admin', 'Seller']:
        if request.method == 'POST':
            form = ProductForm(request.POST, instance=product)
            if form.is_valid():
                form.save()
                messages.success(request, 'Product updated successfully.')
                return redirect('store:product_list')
        else:
            form = ProductForm(instance=product)

        return render(request, 'store/product_form.html', {'form': form})

    messages.error(request, 'You do not have permission to update this product.')
    return redirect('store:product_list')


# Delete a product - restricted to Admin and Seller
@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user.role in ['Admin', 'Seller']:
        if request.method == 'POST':
            product.delete()
            messages.success(request, 'Product deleted successfully.')
            return redirect('store:product_list')
        return render(request, 'store/product_confirm_delete.html', {'product': product})

    messages.error(request, 'You do not have permission to delete this product.')
    return redirect('store:product_list')


# Cart functionality - restricted to Buyers
@login_required
def view_cart(request):
    if request.user.role != 'Buyer':  # Restrict cart view to buyers
        messages.error(request, 'Only buyers can view the cart.')
        return redirect('store:product_list')

    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    total_amount = 0
    for item in cart_items:
        item.total_price = item.quantity * item.product.price
        total_amount += item.total_price

    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease' and cart_item.quantity > 1:
            cart_item.quantity -= 1

        cart_item.save()
        messages.success(request, 'Cart updated successfully.')
        return redirect('view_cart')

    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_amount': total_amount})


# Cart detail - restricted to Buyers
@login_required
def cart_detail(request):
    if request.user.role != 'Buyer':
        messages.error(request, 'Only buyers can view the cart.')
        return redirect('store:product_list')

    cart_items = []
    total_amount = 0

    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart).select_related('product')
    except Cart.DoesNotExist:
        messages.info(request, 'Your cart is empty.')

    total_amount = sum(item.quantity * item.product.price for item in cart_items)

    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_amount': total_amount})


# Add item to cart - restricted to Buyers
@login_required
def add_to_cart(request, product_id):
    if request.user.role != 'Buyer':
        messages.error(request, 'Only buyers can add items to the cart.')
        return redirect('store:product_list')

    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1

    cart_item.save()
    messages.success(request, 'Item added to cart successfully.')
    return redirect('store:product_list')


# Update cart item quantity - restricted to Buyers
@login_required
def update_cart_item(request, item_id):
    if request.user.role != 'Buyer':
        messages.error(request, 'Only buyers can update cart items.')
        return redirect('store:product_list')

    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        if quantity and quantity.isdigit() and int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()
            messages.success(request, 'Cart item updated successfully.')
        else:
            messages.error(request, 'Invalid quantity.')

    return redirect('store:cart_detail')


# Remove item from cart - restricted to Buyers
@login_required
def remove_from_cart(request, item_id):
    if request.user.role != 'Buyer':
        messages.error(request, 'Only buyers can remove items from the cart.')
        return redirect('store:product_list')

    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('store:cart_detail')
