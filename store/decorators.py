"""
Custom decorators for FreshMart role-based access control.
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def customer_required(view_func):
    """
    Allow only authenticated, non-staff users (customers).
    - Unauthenticated → login page
    - Staff/Admin     → home with an error message
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f'/login/?next={request.path}')
        if request.user.is_staff:
            messages.error(
                request,
                'Admins cannot access cart or order features. '
                'Use the Admin Dashboard to manage the store.'
            )
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper
