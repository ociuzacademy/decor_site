from . import views 
from django.urls import path
from .import views
urlpatterns=[
    path('',views.index,name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),   
    #  path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_index/',views.admin_index,name='admin_index'),   
    path('view_user/', views.view_user, name='view_user'),
    path('user_index/',views.user_index,name='user_index'),
    path('products/', views.admin_view_products, name='admin_view_products'),
    path('products_list/', views.admin_add_product, name='admin_add_product'),
    path('product/<int:product_id>/edit/', views.admin_edit_product, name='admin_edit_product'),
    path('products/', views.product_list, name='products_list'),  # Ensure this is named 'product_list'
    path('products/delete/<int:product_id>/', views.admin_delete_product, name='admin_delete_product'),
    path('user_products/', views.view_products, name='view_products'),
    path('user_feedback/', views.leave_feedback, name='feedback'),  # Feedback form URL
    path('view_feedback/', views.view_feedback, name='view_feedback'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-quantity/<int:item_id>/<int:new_quantity>/', views.update_quantity, name='update_quantity'),
    # path('checkout/', views.checkout, name='checkout'),
    # path('confirm_payment/', views.confirm_payment, name='confirm_payment'),
    # path('order_summary/<int:order_id>/', views.order_summary, name='order_summary')
    path('checkout/', views.checkout, name='checkout'),
    path('confirm_payment/', views.confirm_payment, name='confirm_payment'),
    path('order_summary/<int:order_id>/', views.order_summary, name='order_summary'),
    path('order_summary_buy_now/<int:order_id>/', views.order_summary_buy_now, name='order_summary_buy_now'),
    path('notifications/', views.notification_list, name='notifications'),  # New route for notifications
    path('buy_now/<int:product_id>/', views.buy_now, name='buy_now'),  # For "Buy Now"
    path('payment/<int:buy_now_id>/', views.payment_page, name='payment_page'),  # For Payment
   
   
   

    path('admin/designs/', views.admin_design_list, name='admin_design_list'),  # List all designs
    path('admin/designs/add/', views.admin_add_design, name='admin_add_design'),  # Add a new design
    path('admin/designs/edit/', views.edit_design, name='admin_edit_design'),
    path('admin/designs/delete/', views.delete_design, name='admin_delete_design'),

   
    path('designs/', views.designs_by_category, name='designs_by_category'),
    path('admin/add_category/', views.admin_add_category, name='admin_add_category'),
    path('admin/category_list/', views.admin_category_list, name='admin_category_list'),
    path('admin/category/<int:category_id>/edit/', views.admin_edit_category, name='admin_edit_category'),
    path('admin/category/<int:category_id>/delete/', views.admin_delete_category, name='admin_delete_category'),
    path('designs/book/', views.book_design, name='book_design'),  # Handle the booking process
    path('user/bookings/', views.user_bookings, name='user_bookings'),
    path('admin/bookings/', views.admin_bookings, name='admin_bookings'),
    path('user/orders/', views.user_orders, name='user_orders'),
    path('admin/orders/', views.admin_orders, name='admin_orders'),

]






