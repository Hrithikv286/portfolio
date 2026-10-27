"""
Custom error views for ElectroStore
"""
from django.shortcuts import render


def custom_404(request, exception=None):
    """Custom 404 page with Ask Assistant option"""
    context = {
        'error_code': '404',
        'error_title': 'Page Not Found',
        'error_message': "Oops! We couldn't find the page you're looking for.",
        'error_description': 'The page may have been moved, deleted, or the URL may be incorrect.',
    }
    return render(request, 'errors/404.html', context, status=404)


def custom_500(request):
    """Custom 500 page with Ask Assistant option"""
    context = {
        'error_code': '500',
        'error_title': 'Internal Server Error',
        'error_message': 'Something went wrong on our end. We\'re working to fix it.',
        'error_description': 'Our team has been notified. Please try again in a few minutes.',
    }
    return render(request, 'errors/500.html', context, status=500)
