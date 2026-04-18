from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Auth
    path('register/', views.register_view, name='register'),
    path('login/',    views.login_view,    name='login'),
    path('logout/',   views.logout_view,   name='logout'),

    # ── Forgot Password ────────────────────────────────────────────────────────
    path('forgot-password/',
         views.forgot_password_view,
         name='forgot_password'),

    path('forgot-password/sent/',
         views.password_reset_sent_view,
         name='password_reset_sent'),

    path('reset-password/<uidb64>/<token>/',
         views.reset_password_view,
         name='reset_password'),

    path('reset-password/done/',
         views.reset_password_done_view,
         name='reset_password_done'),

    # Cart
    path('cart/',                         views.cart_view,        name='cart'),
    path('cart/add/<int:product_id>/',    views.add_to_cart,      name='add_to_cart'),
    path('cart/remove/<int:cart_id>/',    views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:cart_id>/',    views.update_cart,      name='update_cart'),

    # Payment & Orders
    path('payment/',                         views.payment_view,    name='payment'),
    path('place-order/',                     views.place_order,     name='place_order'),
    path('payment/confirm/<int:order_id>/',  views.payment_confirm, name='payment_confirm'),
    path('payment/simulate/<int:order_id>/', views.simulate_payment,name='simulate_payment'),
    path('orders/',                          views.order_history,   name='order_history'),
    path('orders/cancel/<int:order_id>/',    views.cancel_order,    name='cancel_order'),

    # Admin Dashboard
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Admin Order Management
    path('admin-orders/',                           views.admin_orders,        name='admin_orders'),
    path('admin-orders/update/<int:order_id>/',     views.update_order_status, name='update_order_status'),

    # Admin Product Management
    path('product/edit/<int:product_id>/',   views.edit_product,   name='edit_product'),
    path('product/delete/<int:product_id>/', views.delete_product, name='delete_product'),

    # Reports
    path('reports/csv/',   views.report_csv,   name='report_csv'),
    path('reports/print/', views.report_print, name='report_print'),

    # Chatbot
    path('chatbot/',      views.chatbot_api,       name='chatbot_api'),
    path('chat-history/', views.chat_history_view, name='chat_history'),

    # Pages
    path('about/', views.about_view, name='about'),
]