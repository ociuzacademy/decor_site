from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import *
# Create your views here.
def index(request):
    return render(request,'index.html')




from django.shortcuts import render, redirect
from django.contrib import messages
# from .models import Payment, Register

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        if Register.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('register')

        new_user = Register(name=name, email=email, password=password, address=address, phone=phone)
        new_user.save()

        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')  # Use redirect instead of render

    return render(request, 'register.html')


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import  *

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Check if the email exists for a user first
        try:
            # Check if the email exists in Register (user model)
            user = Register.objects.get(email=email)
            if user.password == password:  # No password hashing, compare directly
                request.session['user_id'] = user.id  # Store user ID in session
                return redirect('user_index')  # Redirect to user homepage or dashboard
            else:
                messages.error(request, "Incorrect password for user.")
        
        except Register.DoesNotExist:
            # If not a user, check if it's an admin
            try:
                admin_user = Admin.objects.get(email=email)
                if admin_user.password == password:  # No password hashing, compare directly
                    request.session['admin_email'] = admin_user.email  # Store admin email in session
                    return redirect('admin_index')  # Redirect to admin dashboard
                else:
                    messages.error(request, "Incorrect password for admin.")
            
            except Admin.DoesNotExist:
                messages.error(request, "No user or admin found with this email.")

    return render(request, 'login.html')




from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Admin

def admin_index(request):
      users = Register.objects.all()  # or use request.user for the logged-in user
      return render(request, 'admin/admin_index.html', {'users': users})
    
from django.shortcuts import render
from .models import Product

def user_index(request):
    # Fetch all products from the database
    products = Product.objects.all()
    return render(request, 'user/user_index.html', {'products': products})
    
def view_user(request):
    # Fetch all users from the Register model
    users = Register.objects.all()
    return render(request, 'admin/view_user.html', {'users': users})


def view_products(request):
    products = Product.objects.all()  # Get all products
    return render(request, 'user/view_product.html', {'products': products})

def admin_delete_product(request, product_id):
    # Fetch the product or 404 if it doesn't exist
    product = get_object_or_404(Product, id=product_id)
    
    # if request.method == 'POST':
        # Delete the product from the database
    product.delete()
        
        # Show a success message
    messages.success(request, 'Product deleted successfully.')
        
        # Redirect to the product list page (adjust the URL name as needed)
    return redirect('products_list')  # Replace 'products_list' with the appropriate URL name
    
    # If the method is GET, render the delete confirmation page
    # return render(request, 'admin/products_delete.html', {'product': product})



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product

def admin_add_product(request):
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')  # Get stock
        image = request.FILES.get('image')
        delivery_date = request.POST.get('delivery_date')
        
        # Validate form data
        if not name or not description or not price or not stock:
            messages.error(request, 'All fields are required.')
        else:
            # Create new product
            product = Product(name=name, description=description, price=price, stock=stock, image=image, delivery_date=delivery_date)
            product.save()

            messages.success(request, 'Product added successfully.')
            return redirect('products_list')
    
    return render(request, 'admin/products_add.html', {'action': 'Add'})

def admin_edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        # Retrieve form data
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')  # Get stock
        image = request.FILES.get('image')
        delivery_date = request.POST.get('delivery_date')
        # Validate form data
        if not name or not description or not price or not stock:
            messages.error(request, 'All fields are required.')
        else:
            # Update the product instance
            product.name = name
            product.description = description
            product.price = price
            product.stock = stock  # Update stock
            product.delivery_date = delivery_date  # Update delivery date
            if image:
                product.image = image

            product.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('products_list')
    
    return render(request, 'admin/products_edit.html', {'product': product, 'action': 'Edit'})

from django.shortcuts import render
from .models import Product

def admin_view_products(request):
    products = Product.objects.all()  # Fetch all products
    return render(request, 'admin/products_list.html', {'products': products})


from .models import Product

def view_products(request):
    products = Product.objects.all()  # Get all products
    return render(request, 'user/view_product.html', {'products': products})

def product_list(request):
    # Get all products from the database
    products = Product.objects.all()
    return render(request, 'admin/products_list.html', {'products': products})
# shop/views.py
from .models import Feedback

def leave_feedback(request):
    if request.method == 'POST':
        # Get data from the form
        name = request.POST.get('name')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        # Validate the form
        if not rating or not comment:
            messages.error(request, 'Rating and comment are required.')
        else:
            try:
                # Save the feedback to the database
                Feedback.objects.create(
                    name=name,
                    rating=int(rating),
                    comment=comment
                )
                messages.success(request, 'Thank you for your feedback!')
                return redirect('feedback')  # Redirect to the feedback page after successful submission
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')

    return render(request, 'user/user_feedback.html')

def view_feedback(request):
    # Fetch all feedback from the database
    feedback_list = Feedback.objects.all()

    return render(request, 'admin/view_feedback.html', {'feedback_list': feedback_list})




from django.shortcuts import get_object_or_404, redirect
from .models import Product, Cart, CartItem
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Product, Cart, CartItem

def add_to_cart(request, product_id):
    # Check if the user is logged in by checking the session
    if 'user_id' not in request.session:
        messages.error(request, "You need to be logged in to add items to the cart.")
        return redirect('login')  # Redirect to login page if not logged in

    product = get_object_or_404(Product, id=product_id)
    
    # Get or create the cart for the user using the user_id from the session
    cart, created = Cart.objects.get_or_create(user_id=request.session['user_id'])

    # Check if the product is already in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        # If the item already exists, increase the quantity
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart')  # Redirect to the product list or cart page




from django.shortcuts import get_object_or_404

def remove_from_cart(request, item_id):
    # Check if the user is logged in
    if 'user_id' not in request.session:
        messages.error(request, "You need to be logged in to remove items from the cart.")
        return redirect('login')

    # Get the cart item to remove
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user_id=request.session['user_id'])

    # Remove the cart item
    cart_item.delete()

    # Redirect to the cart page
    return redirect('view_cart')



def update_quantity(request, item_id, new_quantity):
    # Check if the user is logged in
    if 'user_id' not in request.session:
        messages.error(request, "You need to be logged in to update the quantity.")
        return redirect('login')

    # Ensure new_quantity is valid
    if new_quantity <= 0:
        messages.error(request, "Quantity must be greater than zero.")
        return redirect('view_cart')

    # Get the cart item to update
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user_id=request.session['user_id'])

    # Update the quantity
    cart_item.quantity = new_quantity
    cart_item.save()

    # Redirect to the cart page
    return redirect('view_cart')

from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Cart

def view_cart(request):

    if 'user_id' not in request.session:
        messages.error(request, "Please login to view your cart.")
        return redirect('login')

    cart = Cart.objects.filter(
        user_id=request.session['user_id']
    ).first()

    total_amount = Decimal('0.00')

    if cart:
        for item in cart.items.all():
            total_amount += item.total_price

    return render(request, 'user/view_cart.html', {
        'cart': cart,
        'total_amount': total_amount
    })

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Cart, CartItem, Order
from django.utils import timezone

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Cart
from decimal import Decimal
def checkout(request):

    if 'user_id' not in request.session:
        messages.error(request, "Please login to continue.")
        return redirect('login')

    cart = Cart.objects.filter(
        user_id=request.session['user_id']
    ).first()

    if not cart or not cart.items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('view_cart')

    total_amount = Decimal('0.00')

    for item in cart.items.all():
        total_amount += item.total_price

    return render(request, 'user/checkout.html', {
        'cart': cart,
        'total_amount': total_amount
    })

def order_summary(request, order_id):

    order = Order.objects.prefetch_related(
        'items__product'
    ).get(id=order_id)

    return render(
        request,
        'user/order_summary.html',
        {'order': order}
    )

import uuid
# views.py
from .models import Notification

def confirm_payment(request):

    if 'user_id' not in request.session:
        messages.error(request, "Please login to continue.")
        return redirect('login')

    if request.method != 'POST':
        return redirect('checkout')

    cart = Cart.objects.filter(
        user_id=request.session['user_id']
    ).first()

    if not cart or not cart.items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('view_cart')

    cart_items = list(cart.items.select_related('product'))

    # Calculate total amount
    total_amount = sum(
        (item.product.price * item.quantity for item in cart_items),
        Decimal('0.00')
    )

    # Create Order
    order = Order.objects.create(
        user_id=request.session['user_id'],
        total_amount=total_amount,
        status='Paid'
    )

    # Save order items separately
    for item in cart_items:

        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    # Payment method
    payment_method = request.POST.get('payment_method')

    if payment_method == 'COD':

        Payment.objects.create(
            order=order,
            user_id=request.session['user_id'],
            total_amount=total_amount,
            status='COD'
        )

        messages.success(
            request,
            "Your order has been placed successfully with Cash on Delivery!"
        )

    elif payment_method == 'CARD':

        cardholder_name = request.POST.get('cardholder_name')
        card_number = request.POST.get('card_number')

        if not card_number or len(card_number) < 4:
            messages.error(request, "Invalid card details.")
            return redirect('checkout')

        transaction_id = str(uuid.uuid4())

        masked_card_number = f"**** **** **** {card_number[-4:]}"

        Payment.objects.create(
            order=order,
            user_id=request.session['user_id'],
            total_amount=total_amount,
            status='CARD',
            transaction_id=transaction_id,
            cardholder_name=cardholder_name,
            card_number=masked_card_number
        )

        messages.success(
            request,
            "Your order has been placed successfully with Card Payment!"
        )

    else:
        messages.error(request, "Please select a valid payment method.")
        return redirect('checkout')

    # Reduce product stock
    for item in cart_items:

        product = item.product
        product.stock -= item.quantity
        product.save()

        if product.stock <= 0:
            product.stock = 0
            product.save()

            Notification.objects.create(
                product=product,
                message=f"The product {product.name} is out of stock."
            )

    # Clear cart after saving order items
    cart.items.all().delete()

    return redirect('order_summary', order_id=order.id)

# views.py
from django.shortcuts import render
from .models import Notification

def notification_list(request):
    # Fetch all notifications from the database, ordered by creation date
    notifications = Notification.objects.all().order_by('-created_at')

    return render(request, 'admin/notifications.html', {'notifications': notifications})


# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, BuyNow
from django.utils import timezone


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, BuyNow
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.db import transaction
from decimal import Decimal
from .models import Product, Register, BuyNow, Payment_buy_now


def buy_now(request, product_id):

    if 'user_id' not in request.session:
        messages.error(request, "Please login to buy a product.")
        return redirect('login')

    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':

        try:
            quantity = int(request.POST.get('quantity', 1))
        except (ValueError, TypeError):
            messages.error(request, "Invalid quantity.")
            return redirect('user_index')

        if quantity <= 0:
            messages.error(request, "Quantity must be greater than zero.")
            return redirect('user_index')

        if quantity > product.stock:
            messages.error(
                request,
                f"Only {product.stock} items are available."
            )
            return redirect('user_index')

        user = get_object_or_404(
            Register,
            id=request.session['user_id']
        )

        total_amount = product.price * quantity

        buy_now_entry = BuyNow.objects.create(
            product=product,
            user=user,
            quantity=quantity,
            total_amount=total_amount
        )

        return redirect(
            'payment_page',
            buy_now_id=buy_now_entry.id
        )

    return redirect('user_index')


# views.py
from .models import BuyNow, Payment
import uuid
# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Payment, BuyNow
import uuid

import uuid

from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from .models import BuyNow, Payment_buy_now, Product


def payment_page(request, buy_now_id):

    if 'user_id' not in request.session:
        messages.error(request, "Please login to continue.")
        return redirect('login')

    buy_now = get_object_or_404(
        BuyNow,
        id=buy_now_id,
        user_id=request.session['user_id']
    )

    if request.method == 'POST':

        payment_method = request.POST.get('payment_method')

        if payment_method not in ['COD', 'CARD']:
            messages.error(request, "Please select a valid payment method.")
            return redirect('payment_page', buy_now_id=buy_now.id)

        cardholder_name = None
        masked_card_number = None
        transaction_id = None

        if payment_method == 'CARD':

            cardholder_name = request.POST.get('cardholder_name', '').strip()
            card_number = request.POST.get('card_number', '').replace(' ', '')
            cvv = request.POST.get('cvv', '').strip()
            expiry_date = request.POST.get('expiry_date', '').strip()

            if (
                not cardholder_name
                or not card_number.isdigit()
                or len(card_number) not in [15, 16]
                or not cvv.isdigit()
                or len(cvv) not in [3, 4]
                or not expiry_date
            ):
                messages.error(request, "Please enter valid card details.")
                return redirect('payment_page', buy_now_id=buy_now.id)

            # Demo only: this does not process an actual card payment.
            masked_card_number = f"**** **** **** {card_number[-4:]}"

            transaction_id = str(uuid.uuid4())

        try:
            with transaction.atomic():

                # Lock the product row while checking and updating stock
                product = Product.objects.select_for_update().get(
                    id=buy_now.product_id
                )

                if product.stock < buy_now.quantity:
                    messages.error(
                        request,
                        f"Insufficient stock. Only {product.stock} items available."
                    )
                    return redirect(
                        'payment_page',
                        buy_now_id=buy_now.id
                    )

                # Recalculate amount using the current product price
                total_amount = product.price * buy_now.quantity

                # Create payment record
                Payment_buy_now.objects.create(
                    buy_now=buy_now,
                    user=buy_now.user,
                    total_amount=total_amount,
                    status=payment_method,
                    transaction_id=transaction_id,
                    cardholder_name=cardholder_name,
                    card_number=masked_card_number
                )

                # Reduce stock
                product.stock = F('stock') - buy_now.quantity
                product.save(update_fields=['stock'])

                messages.success(
                    request,
                    "Your order has been placed successfully!"
                )

        except Product.DoesNotExist:
            messages.error(request, "Product not found.")
            return redirect('user_index')

        return redirect(
            'order_summary_buy_now',
            order_id=buy_now.id
        )

    return render(
        request,
        'user/payment_page.html',
        {'buy_now': buy_now}
    )


def order_summary_buy_now(request, order_id):

    if 'user_id' not in request.session:
        messages.error(request, "Please login to view your order.")
        return redirect('login')

    order = get_object_or_404(
        BuyNow.objects.select_related('product', 'user'),
        id=order_id,
        user_id=request.session['user_id']
    )

    payment = Payment_buy_now.objects.filter(
        buy_now=order
    ).first()

    return render(request, 'user/order_summary_buy_now.html', {
        'order': order,
        'payment': payment
    })

from django.http import HttpResponse


from django.shortcuts import render
from .models import Design

# View for displaying all designs
# def view_design(request):
#     designs = Design.objects.all()  # Fetch all designs from the database
#     return render(request, 'user/view_design.html', {'designs': designs})

def designs_by_category(request):
    # Get the category from the query parameters
    category_name = request.GET.get('category', '')

    # Filter designs by category if one is selected
    if category_name:
        designs = Design.objects.filter(category__category=category_name)
    else:
        designs = Design.objects.all()

    # Get all categories to display in the filter
    categories = Category.objects.all()

    return render(request, 'user/view_design.html', {
        'designs': designs,
        'categories': categories
    })

from .models import Design  # Import your Design model
def design_list(request):
    designs = Design.objects.all()
    # Your logic here
    return render(request, 'design_list.html',{'designs': designs})


from .models import Design  # Assuming you have a Design model

# View to display all designs
def admin_design_list(request):
    designs = Design.objects.all()  # Fetch all designs
    return render(request, 'admin/design_list.html', {'designs': designs})

# def new_func(request, design):
#     return render(request, 'admin/design_list.html', {'designs': design})

# View to add a new design
def admin_add_design(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        image = request.FILES.get('image')  # Handle file upload
        category_id = request.POST.get('category')  # Get selected category ID
        delivery_date = request.POST.get('delivery_date')  # Get delivery date

        # Get the Category object
        category = Category.objects.get(id=category_id)

        # Save new design to the database
        Design.objects.create(
            name=name, 
            description=description, 
            price=price, 
            stock=stock,
            image=image, 
            category=category,
            delivery_date=delivery_date
        )

        return redirect('admin_design_list')  # Redirect to the design list view
    
    categories = Category.objects.all()  # Get all categories
    return render(request, 'admin/add_design.html', {'categories': categories})

# View to edit an existing design
def edit_design(request):
    id=request.GET.get('id')
    design = get_object_or_404(Design, id=id)

    if request.method == "POST":
        design.name = request.POST.get('name')
        design.description = request.POST.get('description')
        design.price = request.POST.get('price')
        design.stock = request.POST.get('stock')
        design.delivery_date = request.POST.get('delivery_date')
        design.image = request.FILES.get('image', design.image)  # Only update image if provided
        design.category = Category.objects.get(id=request.POST.get('category'))
        design.save()

        return redirect('admin_design_list')  # Redirect to the design list view

    return render(request, 'admin/admin_edit_design.html', {'designs': design})  # Return form pre-filled with the design details

# View to delete a design
def delete_design(request):
    id=request.GET.get('id')
    design = get_object_or_404(Design, id=id)
    design.delete()  # Delete the design from the database

    return redirect('decorapp:admin_design_list')  # Redirect to the design list view

def admin_add_category(request):
    if request.method == "POST":
        category_name = request.POST.get('category')  # Get the category name from the form

        # Create and save the new category
        Category.objects.create(category=category_name)

        return redirect('admin_category_list')  # Redirect to the category list page
    
    return render(request, 'admin/add_category.html')

def admin_category_list(request):
    categories = Category.objects.all()  # Get all categories
    return render(request, 'admin/category_list.html', {'categories': categories})

def admin_edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category_name = request.POST.get('category', '').strip()
        if not category_name:
            messages.error(request, 'Category name is required.')
            return render(request, 'admin/category_edit.html', {'category': category})
        category.category = category_name
        category.save()
        messages.success(request, 'Category updated successfully.')
        return redirect('admin_category_list')
    return render(request, 'admin/category_edit.html', {'category': category})


def admin_delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    messages.success(request, 'Category deleted successfully.')
    return redirect('admin_category_list')
    
def book_design(request):
    if request.method == "POST":
        # Get the design_id from the POST data
        design_id = request.POST.get('design_id')
        design = Design.objects.get(id=design_id)

        # Retrieve user information from the session
        user_id = request.session.get('user_id')

        if user_id:
            user = Register.objects.get(id=user_id)

            if design.stock <= 0 or design.is_available == False:
                messages.error(request, "This design is out of stock.")
                return redirect('designs_by_category')

            # These lines must be HERE (same level as the if above), not inside the if
            booking = Booking(design=design, user=user)
            booking.save()

            design.stock -= 1
            design.save()

            return redirect('designs_by_category')

        else:
            return redirect('login')

    # If not a POST request, redirect to the design details page
    return redirect('designs_by_category')
from django.shortcuts import render, redirect
from django.db.models import Prefetch
from .models import Order, OrderItem, BuyNow, Payment, Payment_buy_now


def user_orders(request):
    if 'user_id' not in request.session:
        return redirect('login')

    user_id = request.session['user_id']

    # Cart purchases
    cart_orders = Order.objects.filter(
        user_id=user_id
    ).prefetch_related(
        'items__product'
    ).order_by('-created_at')

    # Direct Buy Now purchases
    buy_now_orders = BuyNow.objects.filter(
        user_id=user_id
    ).select_related(
        'product'
    ).prefetch_related(
        'payments'
    ).order_by('-created_at')

    all_orders = []

    for order in cart_orders:
        payment = Payment.objects.filter(
            order=order,
            user_id=user_id
        ).order_by('-created_at').first()

        first_item = order.items.first()

        all_orders.append({
            'id': order.id,
            'order_type': 'Cart Purchase',
            'created_at': order.created_at,
            'total_amount': order.total_amount,
            'status': order.status,
            'payment': payment,
            'delivery_date': (
                first_item.product.delivery_date if first_item else None
            ),
            'url_name': 'order_summary',
        })

    for order in buy_now_orders:
        payment = order.payments.filter(
            user_id=user_id
        ).order_by('-created_at').first()

        all_orders.append({
            'id': order.id,
            'order_type': 'Buy Now',
            'created_at': order.created_at,
            'total_amount': order.total_amount,
            'status': 'Placed' if payment else 'Pending',
            'payment': payment,
            'delivery_date': order.product.delivery_date,
            'url_name': 'order_summary_buy_now',
        })

    # Show latest purchases first
    all_orders.sort(
        key=lambda item: item['created_at'],
        reverse=True
    )

    return render(
        request,
        'user/user_orders.html',
        {'orders': all_orders}
    )

def user_bookings(request):
    # Check if the user_id exists in session
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')  # Redirect to login page if the user isn't logged in via session

    # Retrieve the user from the session
    user = Register.objects.get(id=user_id)

    # Get all bookings for this user
    bookings = Booking.objects.filter(user=user)

    # Render the user bookings page with the booking details
    return render(request, 'user/user_bookings.html', {'bookings': bookings})


def admin_bookings(request):
    # Get all bookings with related user details
    bookings = Booking.objects.all().select_related('user')  # Using select_related for optimized queries

    # Render the admin bookings page with the booking details
    return render(request, 'admin/admin_bookings.html', {'bookings': bookings})

def admin_orders(request):
    orders = Order.objects.all().select_related('user').prefetch_related('payment_set', 'items__product').order_by('-created_at')
    orders = list(orders)
    for order in orders:
        order.payment = order.payment_set.first()
    return render(request, 'admin/admin_orders.html', {'orders': orders})
