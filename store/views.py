"""
Store app views - Home, Products, Product Detail, FAQ, Health Check, Error pages
"""
import logging
import requests
import time
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Category, Product, FAQ, ErrorCode, SupportTicket

logger = logging.getLogger('store')


def home(request):
    """Homepage - Featured products, categories, and deals"""
    categories = Category.objects.filter(is_active=True)[:8]
    featured_products = Product.objects.filter(is_featured=True, is_active=True)[:8]
    new_arrivals = Product.objects.filter(is_new_arrival=True, is_active=True)[:8]
    best_sellers = Product.objects.filter(is_active=True, rating__gte=4.0).order_by('-review_count')[:8]

    # Weather widget via OpenWeatherMap (third-party API with timeout + fallback)
    weather_data = get_weather_data()

    context = {
        'categories': categories,
        'featured_products': featured_products,
        'new_arrivals': new_arrivals,
        'best_sellers': best_sellers,
        'weather': weather_data,
    }
    return render(request, 'store/home.html', context)


def get_weather_data():
    """Fetch weather data from OpenWeatherMap API with timeout and fallback"""
    api_key = settings.OPENWEATHER_API_KEY
    timeout = settings.OPENWEATHER_API_TIMEOUT

    if not api_key:
        return get_weather_fallback()

    try:
        response = requests.get(
            'https://api.openweathermap.org/data/2.5/weather',
            params={'q': 'Chennai', 'appid': api_key, 'units': 'metric'},
            timeout=timeout
        )
        response.raise_for_status()
        data = response.json()
        return {
            'city': data['name'],
            'temp': round(data['main']['temp']),
            'description': data['weather'][0]['description'].title(),
            'icon': data['weather'][0]['icon'],
            'humidity': data['main']['humidity'],
            'source': 'live',
        }
    except requests.Timeout:
        logger.warning("OpenWeatherMap API timeout - using fallback data")
        return get_weather_fallback()
    except requests.RequestException as e:
        logger.warning(f"OpenWeatherMap API error: {e} - using fallback data")
        return get_weather_fallback()


def get_weather_fallback():
    """Fallback weather data when API is unavailable"""
    return {
        'city': 'Chennai',
        'temp': 32,
        'description': 'Partly Cloudy',
        'icon': '02d',
        'humidity': 70,
        'source': 'fallback',
    }


def products(request):
    """Product listing page with filters and search"""
    all_products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)

    # Filters
    category_slug = request.GET.get('category', '')
    search_query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', '-created_at')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    in_stock = request.GET.get('in_stock', '')

    if category_slug:
        all_products = all_products.filter(category__slug=category_slug)

    if search_query:
        all_products = all_products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(brand__name__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )

    if min_price:
        try:
            all_products = all_products.filter(price__gte=float(min_price))
        except ValueError:
            pass

    if max_price:
        try:
            all_products = all_products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    if in_stock == 'yes':
        all_products = all_products.filter(stock__gt=0)

    # Sort
    valid_sorts = ['-created_at', 'price', '-price', '-rating', 'name']
    if sort_by in valid_sorts:
        all_products = all_products.order_by(sort_by)

    # Pagination
    paginator = Paginator(all_products, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    selected_category = None
    if category_slug:
        try:
            selected_category = Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            pass

    context = {
        'products': page_obj,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query,
        'sort_by': sort_by,
        'total_count': all_products.count(),
    }
    return render(request, 'store/products.html', context)


def product_detail(request, slug):
    """Product detail page"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'store/product_detail.html', context)


def faq(request):
    """FAQ page - All FAQs from SQL database"""
    faqs = FAQ.objects.filter(is_active=True)

    # Group by category
    faq_categories = {}
    category_labels = dict(FAQ.CATEGORY_CHOICES)

    for faq_item in faqs:
        cat = faq_item.category
        if cat not in faq_categories:
            faq_categories[cat] = {
                'label': category_labels.get(cat, cat),
                'items': []
            }
        faq_categories[cat]['items'].append(faq_item)

    context = {
        'faq_categories': faq_categories,
        'total_faqs': faqs.count(),
    }
    return render(request, 'store/faq.html', context)


def error_codes(request):
    """Error codes explanation page"""
    error_codes_list = ErrorCode.objects.all()
    context = {'error_codes': error_codes_list}
    return render(request, 'store/error_codes.html', context)


def health_check(request):
    """Health check endpoint - checks DB, MongoDB, and APIs"""
    import datetime
    from django.db import connection

    health = {
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'version': '1.0.0',
        'checks': {}
    }

    # Database check
    try:
        connection.ensure_connection()
        product_count = Product.objects.count()
        health['checks']['database'] = {
            'status': 'ok',
            'products': product_count
        }
    except Exception as e:
        health['status'] = 'unhealthy'
        health['checks']['database'] = {'status': 'error', 'message': str(e)}

    # MongoDB check
    try:
        from chat.mongo_client import get_mongodb
        db = get_mongodb()
        if db is not None:
            db.command('ping')
            health['checks']['mongodb'] = {'status': 'ok'}
        else:
            health['checks']['mongodb'] = {'status': 'not_configured'}
    except Exception as e:
        health['checks']['mongodb'] = {'status': 'error', 'message': str(e)}

    # Gemini API check
    health['checks']['gemini_api'] = {
        'status': 'configured' if settings.GEMINI_API_KEY else 'not_configured'
    }

    # Weather API check
    health['checks']['weather_api'] = {
        'status': 'configured' if settings.OPENWEATHER_API_KEY else 'not_configured'
    }

    status_code = 200 if health['status'] == 'healthy' else 503
    return JsonResponse(health, status=status_code)


def simulate_error(request, code):
    """Simulate different HTTP error codes for demonstration"""
    error_map = {
        '400': (400, '400 Bad Request', 'The server could not understand the request.'),
        '401': (401, '401 Unauthorized', 'Authentication is required.'),
        '403': (403, '403 Forbidden', 'You do not have permission to access this resource.'),
        '404': (404, '404 Not Found', 'The requested resource was not found.'),
        '429': (429, '429 Too Many Requests', 'You have exceeded the rate limit.'),
        '500': (500, '500 Internal Server Error', 'Something went wrong on the server.'),
        '503': (503, '503 Service Unavailable', 'The service is temporarily unavailable.'),
        'ES001': (422, 'ES001 Payment Declined', 'Your payment could not be processed. Please check your card details.'),
    }

    if str(code) in error_map:
        status, title, message = error_map[str(code)]
        context = {
            'error_code': str(code),
            'error_title': title,
            'error_message': message,
            'error_description': f'This is a demonstration of error code {code}.',
        }
        template = 'errors/generic_error.html'
        if str(code) == '404':
            template = 'errors/404.html'
        elif str(code) == '500':
            template = 'errors/500.html'
        return render(request, template, context, status=status)

    return render(request, 'errors/404.html', {
        'error_code': '404',
        'error_title': 'Error Not Found',
        'error_message': 'The requested error code does not exist.',
        'error_description': '',
    }, status=404)


def about(request):
    """About page"""
    return render(request, 'store/about.html')


def contact(request):
    """Contact page"""
    if request.method == 'POST':
        # Handle contact form
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')

        if name and email and message:
            SupportTicket.objects.create(
                user_name=name,
                user_email=email,
                user_message=message,
                priority='medium',
            )
            return JsonResponse({'success': True, 'message': 'Your message has been received!'})

        return JsonResponse({'success': False, 'message': 'Please fill all fields.'}, status=400)

    return render(request, 'store/contact.html')
