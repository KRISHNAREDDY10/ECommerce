import stripe
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required 
from store.models import Cart, CartItem 
from checkout.models import Order
from checkout.forms import OrderForm

# Set Stripe API Key
stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required  # Ensures the user is logged in
def checkout(request):
    # Get the cart and cart items for the authenticated user
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.cart_items.all()  # Assuming related_name='cart_items'
    except Cart.DoesNotExist:
        messages.error(request, "Your cart is empty.")
        return redirect('store:product_list')

    # Handle form submission
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.status = 'Pending'
            order.save()

            # Create Stripe Checkout Session
            line_items = []
            for item in cart_items:
                line_items.append({
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': item.product.name,
                        },
                        'unit_amount': int(item.product.price * 100),  # Stripe requires amount in cents
                    },
                    'quantity': item.quantity,
                })

            try:
                # Create Stripe Checkout session
                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=line_items,
                    mode='payment',
                    success_url=request.build_absolute_uri('/checkout/success/'),
                    cancel_url=request.build_absolute_uri('/checkout/cancel/'),
                )
                return redirect(session.url, code=303)  # Redirect to Stripe's checkout page
            except stripe.error.StripeError as e:
                messages.error(request, f"Stripe error: {str(e)}")
                return redirect('checkout')

    else:
        form = OrderForm()

    # Render checkout page with the form and cart items
    return render(request, 'checkout/checkout.html', {'form': form, 'cart_items': cart_items})

@login_required
def checkout_success(request):
    try:
        # Fetch the user's cart
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        # Clear the cart items after successful payment
        cart_items.delete()
        messages.success(request, 'Payment completed successfully! Your cart has been cleared.')
    except Cart.DoesNotExist:
        messages.error(request, 'No cart found for this user.')

    # Render the checkout success template
    return render(request, 'checkout/checkout_success.html')

# Cancel page
def checkout_cancel(request):
    messages.error(request, 'Payment was cancelled.')
    return render(request, 'checkout/checkout_cancel.html')
