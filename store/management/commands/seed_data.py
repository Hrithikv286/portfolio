"""
Management command to populate the database with sample data
Run: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from store.models import Category, Brand, Product, FAQ, ErrorCode


class Command(BaseCommand):
    help = 'Seed the database with initial data for ElectroStore'

    def handle(self, *args, **options):
        self.stdout.write('🌱 Seeding ElectroStore database...')

        self.create_categories()
        self.create_brands()
        self.create_products()
        self.create_faqs()
        self.create_error_codes()

        self.stdout.write(self.style.SUCCESS('✅ Database seeded successfully!'))

    def create_categories(self):
        categories = [
            {'name': 'Smartphones', 'icon': 'fa-mobile-alt', 'description': 'Latest smartphones and mobile phones'},
            {'name': 'Laptops', 'icon': 'fa-laptop', 'description': 'Laptops for work, gaming, and creativity'},
            {'name': 'Televisions', 'icon': 'fa-tv', 'description': 'Smart TVs from top brands'},
            {'name': 'Audio Devices', 'icon': 'fa-headphones', 'description': 'Headphones, earbuds, and speakers'},
            {'name': 'Gaming', 'icon': 'fa-gamepad', 'description': 'Gaming consoles, controllers, and accessories'},
            {'name': 'Smart Home', 'icon': 'fa-home', 'description': 'Smart speakers, cameras, and home automation'},
            {'name': 'Cameras', 'icon': 'fa-camera', 'description': 'DSLR, mirrorless, and action cameras'},
            {'name': 'Accessories', 'icon': 'fa-plug', 'description': 'Chargers, cables, cases, and more'},
        ]

        for cat_data in categories:
            Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'icon': cat_data['icon'],
                    'description': cat_data['description'],
                }
            )
        self.stdout.write(f'  ✓ Created {len(categories)} categories')

    def create_brands(self):
        brands = ['Apple', 'Samsung', 'Sony', 'LG', 'OnePlus', 'Dell', 'HP', 'Asus',
                  'Lenovo', 'Xiaomi', 'Realme', 'JBL', 'Boat', 'Philips', 'Canon', 'Nikon']

        for brand_name in brands:
            Brand.objects.get_or_create(name=brand_name)

        self.stdout.write(f'  ✓ Created {len(brands)} brands')

    def create_products(self):
        products_data = [
            # Smartphones
            {
                'name': 'iPhone 15 Pro Max',
                'category': 'Smartphones', 'brand': 'Apple',
                'price': 159900, 'original_price': 174900,
                'stock': 50, 'rating': 4.8, 'review_count': 2341,
                'is_featured': True, 'is_new_arrival': True,
                'short_description': '48MP Camera, A17 Pro Chip, Titanium Design',
                'description': 'The iPhone 15 Pro Max is Apple\'s most advanced iPhone. Features the A17 Pro chip, a 48MP Main camera with 5x optical zoom, and a stunning titanium design with Action button.',
                'image_url': 'https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=400',
                'specifications': {'Display': '6.7" Super Retina XDR', 'Processor': 'A17 Pro', 'RAM': '8GB', 'Storage': '256GB', 'Battery': '4422mAh'},
            },
            {
                'name': 'Samsung Galaxy S24 Ultra',
                'category': 'Smartphones', 'brand': 'Samsung',
                'price': 134999, 'original_price': 149999,
                'stock': 35, 'rating': 4.7, 'review_count': 1876,
                'is_featured': True, 'is_new_arrival': True,
                'short_description': '200MP Camera, S-Pen, 12GB RAM',
                'description': 'Samsung Galaxy S24 Ultra with 200MP camera, built-in S-Pen, Snapdragon 8 Gen 3, and 5000mAh battery with 45W fast charging.',
                'image_url': 'https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=400',
                'specifications': {'Display': '6.8" Dynamic AMOLED 2X', 'Processor': 'Snapdragon 8 Gen 3', 'RAM': '12GB', 'Storage': '256GB', 'Battery': '5000mAh'},
            },
            {
                'name': 'OnePlus 12',
                'category': 'Smartphones', 'brand': 'OnePlus',
                'price': 64999, 'original_price': 69999,
                'stock': 80, 'rating': 4.5, 'review_count': 987,
                'is_featured': False, 'is_new_arrival': True,
                'short_description': 'Snapdragon 8 Gen 3, 100W Charging',
                'description': 'OnePlus 12 with Snapdragon 8 Gen 3, Hasselblad camera system, 100W SUPERVOOC charging, and 50W wireless charging.',
                'image_url': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400',
                'specifications': {'Display': '6.82" LTPO AMOLED', 'Processor': 'Snapdragon 8 Gen 3', 'RAM': '16GB', 'Storage': '512GB', 'Battery': '5400mAh'},
            },
            # Laptops
            {
                'name': 'MacBook Pro 14" M3 Pro',
                'category': 'Laptops', 'brand': 'Apple',
                'price': 199900, 'original_price': 214900,
                'stock': 20, 'rating': 4.9, 'review_count': 542,
                'is_featured': True, 'is_new_arrival': False,
                'short_description': 'M3 Pro Chip, 18GB RAM, 18hr Battery',
                'description': 'MacBook Pro with M3 Pro chip delivers exceptional performance for demanding workflows. 18GB unified memory, 512GB SSD, and Liquid Retina XDR display.',
                'image_url': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400',
                'specifications': {'Processor': 'Apple M3 Pro', 'RAM': '18GB', 'Storage': '512GB SSD', 'Display': '14.2" Liquid Retina XDR', 'Battery': '18 hours'},
            },
            {
                'name': 'Dell XPS 15',
                'category': 'Laptops', 'brand': 'Dell',
                'price': 159990, 'original_price': 174990,
                'stock': 15, 'rating': 4.6, 'review_count': 321,
                'is_featured': True, 'is_new_arrival': False,
                'short_description': 'Intel Core i7, NVIDIA RTX 4060, OLED Display',
                'description': 'Dell XPS 15 with Intel Core i7-13700H, NVIDIA GeForce RTX 4060, 16GB RAM, 512GB SSD, and stunning 15.6" OLED display.',
                'image_url': 'https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=400',
                'specifications': {'Processor': 'Intel Core i7-13700H', 'RAM': '16GB DDR5', 'GPU': 'NVIDIA RTX 4060', 'Storage': '512GB NVMe SSD', 'Display': '15.6" OLED 3.5K'},
            },
            # TVs
            {
                'name': 'Samsung 65" 4K QLED TV',
                'category': 'Televisions', 'brand': 'Samsung',
                'price': 109990, 'original_price': 139990,
                'stock': 12, 'rating': 4.7, 'review_count': 654,
                'is_featured': True, 'is_new_arrival': False,
                'short_description': '65" QLED, 4K, 120Hz, Smart TV',
                'description': 'Samsung 65" QLED 4K Smart TV with Quantum Dot technology, 120Hz refresh rate, Object Tracking Sound, and Tizen OS.',
                'image_url': 'https://images.unsplash.com/photo-1593359677879-a4bb92f4834c?w=400',
                'specifications': {'Size': '65"', 'Resolution': '4K UHD', 'Display': 'QLED', 'Refresh Rate': '120Hz', 'Smart TV': 'Tizen OS'},
            },
            # Audio
            {
                'name': 'Sony WH-1000XM5',
                'category': 'Audio Devices', 'brand': 'Sony',
                'price': 29990, 'original_price': 34990,
                'stock': 100, 'rating': 4.8, 'review_count': 3241,
                'is_featured': True, 'is_new_arrival': False,
                'short_description': 'Industry Best ANC, 30hr Battery',
                'description': 'Sony WH-1000XM5 wireless noise-cancelling headphones with industry-leading ANC, 30-hour battery life, multipoint connection, and Hi-Res Audio.',
                'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400',
                'specifications': {'Type': 'Over-ear', 'Driver': '30mm', 'Frequency': '4Hz-40,000Hz', 'Battery': '30 hours', 'Charging': 'USB-C'},
            },
            {
                'name': 'Apple AirPods Pro 2nd Gen',
                'category': 'Audio Devices', 'brand': 'Apple',
                'price': 24900, 'original_price': 26900,
                'stock': 150, 'rating': 4.7, 'review_count': 2109,
                'is_featured': False, 'is_new_arrival': True,
                'short_description': 'Active Noise Cancellation, H2 Chip',
                'description': 'AirPods Pro with H2 chip, Adaptive Transparency, Personalized Spatial Audio, and MagSafe Charging Case with Built-in Speaker.',
                'image_url': 'https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?w=400',
                'specifications': {'Chip': 'Apple H2', 'ANC': 'Active Noise Cancellation', 'Battery': '6hr + 30hr case', 'Resistance': 'IPX4'},
            },
            # Gaming
            {
                'name': 'PlayStation 5',
                'category': 'Gaming', 'brand': 'Sony',
                'price': 54990, 'original_price': 59990,
                'stock': 25, 'rating': 4.9, 'review_count': 5432,
                'is_featured': True, 'is_new_arrival': False,
                'short_description': '4K Gaming, 120fps, Ultra HD Blu-ray',
                'description': 'PS5 with custom 825GB SSD, 4K gaming up to 120fps, ray tracing, Ultra HD Blu-ray, and DualSense wireless controller with haptic feedback.',
                'image_url': 'https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?w=400',
                'specifications': {'CPU': '8-core AMD Zen 2', 'GPU': 'AMD RDNA 2', 'RAM': '16GB GDDR6', 'Storage': '825GB SSD', 'Resolution': 'Up to 8K'},
            },
            # Smart Home
            {
                'name': 'Amazon Echo Dot 5th Gen',
                'category': 'Smart Home', 'brand': 'Philips',
                'price': 4999, 'original_price': 5999,
                'stock': 200, 'rating': 4.4, 'review_count': 876,
                'is_featured': False, 'is_new_arrival': True,
                'short_description': 'Alexa Smart Speaker, Improved Sound',
                'description': 'Echo Dot 5th Gen with Alexa, improved sound quality, temperature sensor, motion detection, and smart home hub capabilities.',
                'image_url': 'https://images.unsplash.com/photo-1543512214-318c7553f230?w=400',
                'specifications': {'Speaker': '1.73" front-firing', 'Connectivity': 'Wi-Fi, Bluetooth', 'Features': 'Alexa, Temperature Sensor', 'Power': '15W adapter'},
            },
            # Camera
            {
                'name': 'Canon EOS R6 Mark II',
                'category': 'Cameras', 'brand': 'Canon',
                'price': 234990, 'original_price': 259990,
                'stock': 8, 'rating': 4.8, 'review_count': 234,
                'is_featured': False, 'is_new_arrival': False,
                'short_description': '40fps Burst, 4K 60p Video, IBIS',
                'description': 'Canon EOS R6 Mark II mirrorless camera with 40fps burst shooting, 4K 60p video, 6.5-stop IBIS, and advanced AF system.',
                'image_url': 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=400',
                'specifications': {'Sensor': '24.2MP Full-Frame CMOS', 'ISO': '100-102400', 'Video': '4K 60p', 'AF': 'Dual Pixel CMOS AF II', 'Burst': '40fps'},
            },
            # Accessories
            {
                'name': 'Anker 65W USB-C Charger',
                'category': 'Accessories', 'brand': 'Philips',
                'price': 2499, 'original_price': 2999,
                'stock': 500, 'rating': 4.6, 'review_count': 4321,
                'is_featured': False, 'is_new_arrival': False,
                'short_description': '65W GaN Charger, 3-port, Compact',
                'description': 'Anker 65W 3-Port USB-C Charger with GaN technology. Charges laptop, phone, and tablet simultaneously. Ultra-compact design.',
                'image_url': 'https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=400',
                'specifications': {'Power': '65W total', 'Ports': '2x USB-C, 1x USB-A', 'Technology': 'GaN II', 'Safety': 'Overheat protection'},
            },
        ]

        cats = {c.name: c for c in Category.objects.all()}
        brands = {b.name: b for b in Brand.objects.all()}

        created = 0
        for pd in products_data:
            cat = cats.get(pd['category'])
            brand = brands.get(pd['brand'])
            if cat:
                product, created_flag = Product.objects.get_or_create(
                    name=pd['name'],
                    defaults={
                        'category': cat,
                        'brand': brand,
                        'price': pd['price'],
                        'original_price': pd.get('original_price'),
                        'stock': pd['stock'],
                        'rating': pd['rating'],
                        'review_count': pd['review_count'],
                        'is_featured': pd.get('is_featured', False),
                        'is_new_arrival': pd.get('is_new_arrival', False),
                        'short_description': pd.get('short_description', ''),
                        'description': pd['description'],
                        'image_url': pd.get('image_url', ''),
                        'specifications': pd.get('specifications', {}),
                    }
                )
                if created_flag:
                    created += 1

        self.stdout.write(f'  ✓ Created {created} products')

    def create_faqs(self):
        faqs_data = [
            # Ordering & Payment
            {
                'question': 'What payment methods does ElectroStore accept?',
                'answer': 'ElectroStore accepts multiple payment methods including:\n• UPI (GPay, PhonePe, Paytm)\n• Credit & Debit Cards (Visa, Mastercard, RuPay)\n• Net Banking (all major banks)\n• EMI options (No-Cost EMI available)\n• Cash on Delivery (available for orders below ₹50,000)',
                'category': 'ordering',
                'order': 1,
            },
            {
                'question': 'Can I cancel my order after placing it?',
                'answer': 'Yes, you can cancel your order within 24 hours of placing it for a full refund. After 24 hours, cancellation is subject to the product status. If the order is already shipped, you can initiate a return once you receive it. To cancel, go to My Orders → Select Order → Cancel Order.',
                'category': 'ordering',
                'order': 2,
            },
            {
                'question': 'Is it safe to use my credit/debit card on ElectroStore?',
                'answer': 'Absolutely! ElectroStore uses 256-bit SSL encryption to protect your payment information. We are PCI DSS compliant and never store your complete card details. All transactions go through secure payment gateways like Razorpay and Stripe.',
                'category': 'ordering',
                'order': 3,
            },
            # Shipping & Delivery
            {
                'question': 'How long does delivery take?',
                'answer': 'Delivery times vary by location:\n• Metro cities (Mumbai, Delhi, Bangalore): 1-2 business days\n• Tier 2 cities: 2-3 business days\n• Other locations: 3-5 business days\n• Remote areas: 5-7 business days\n\nFree shipping on all orders above ₹999.',
                'category': 'shipping',
                'order': 4,
            },
            {
                'question': 'How can I track my order?',
                'answer': 'You can track your order in multiple ways:\n1. Visit My Orders section in your account\n2. Click the tracking link in your order confirmation email\n3. Use the AWB number from the shipping SMS with our courier partner\'s website\n4. Ask our AI assistant with your order ID',
                'category': 'shipping',
                'order': 5,
            },
            {
                'question': 'Do you offer free shipping?',
                'answer': 'Yes! ElectroStore offers free standard shipping on all orders above ₹999. For orders below ₹999, a flat shipping fee of ₹49 is applied. Express delivery (next-day) is available for ₹149 in metro cities.',
                'category': 'shipping',
                'order': 6,
            },
            # Returns & Refunds
            {
                'question': 'What is ElectroStore\'s return policy?',
                'answer': 'ElectroStore offers a 7-day return policy from the date of delivery. Products must be:\n• Unused and in original condition\n• In original packaging with all accessories\n• Not physically damaged\n\nNote: Software, games, and consumables cannot be returned. Large appliances have different return windows.',
                'category': 'returns',
                'order': 7,
            },
            {
                'question': 'How long does it take to get a refund?',
                'answer': 'Refund timelines after return pickup:\n• UPI/Net Banking: 3-5 business days\n• Credit/Debit Card: 5-7 business days\n• EMI: 7-10 business days\n• Cash on Delivery: Bank transfer in 5-7 days\n\nYou\'ll receive an email confirmation when refund is initiated.',
                'category': 'returns',
                'order': 8,
            },
            # Product & Technical
            {
                'question': 'Are the products covered under warranty?',
                'answer': 'Yes! All electronics at ElectroStore come with:\n• 1-year manufacturer warranty (standard for all products)\n• Extended warranty available at checkout (1-3 years)\n• Accidental damage protection available\n\nFor warranty claims, visit our service centers or call our support team. Keep your invoice handy for warranty claims.',
                'category': 'warranty',
                'order': 9,
            },
            {
                'question': 'What does the error code 404 mean on ElectroStore?',
                'answer': 'A 404 error means the page you\'re looking for doesn\'t exist or has been moved. This could happen when:\n• You clicked on an old/expired link\n• A product has been discontinued\n• There\'s a typo in the URL\n\nSolution: Use the search bar to find what you\'re looking for, or browse our categories.',
                'category': 'product',
                'order': 10,
            },
            # Account
            {
                'question': 'How do I reset my password?',
                'answer': 'To reset your password:\n1. Click "Forgot Password" on the login page\n2. Enter your registered email address\n3. Check your email for the reset link (valid for 1 hour)\n4. Click the link and create a new password\n\nIf you don\'t receive the email, check your spam folder or contact support.',
                'category': 'account',
                'order': 11,
            },
            {
                'question': 'Can I use ElectroStore without creating an account?',
                'answer': 'Yes, you can browse and make purchases as a guest. However, creating an account gives you benefits like:\n• Order tracking\n• Wish lists and saved carts\n• Faster checkout\n• Order history\n• Exclusive member discounts\n• Easy returns management',
                'category': 'account',
                'order': 12,
            },
            # General
            {
                'question': 'Does ElectroStore have a physical store?',
                'answer': 'ElectroStore is primarily an online electronics retailer. We have experience centers in select cities:\n• Bangalore: Koramangala & Whitefield\n• Mumbai: Andheri & Powai\n• Delhi: Connaught Place\n\nThese centers allow you to experience products before purchasing online.',
                'category': 'general',
                'order': 13,
            },
        ]

        created = 0
        for faq_data in faqs_data:
            _, created_flag = FAQ.objects.get_or_create(
                question=faq_data['question'],
                defaults={
                    'answer': faq_data['answer'],
                    'category': faq_data['category'],
                    'order': faq_data['order'],
                }
            )
            if created_flag:
                created += 1

        self.stdout.write(f'  ✓ Created {created} FAQs (total: {len(faqs_data)})')

    def create_error_codes(self):
        error_codes_data = [
            {
                'code': '400',
                'title': 'Bad Request',
                'description': 'The server could not understand the request due to invalid syntax. Your request may have invalid parameters or malformed data.',
                'solution': 'Check your request parameters and ensure all required fields are filled correctly. Clear your browser cache and try again.',
                'severity': 'warning',
                'is_http_standard': True,
            },
            {
                'code': '401',
                'title': 'Unauthorized',
                'description': 'You need to authenticate before accessing this resource. Your session may have expired or you\'re not logged in.',
                'solution': 'Please log in to your ElectroStore account. If you\'re already logged in, try logging out and logging back in.',
                'severity': 'warning',
                'is_http_standard': True,
            },
            {
                'code': '403',
                'title': 'Forbidden',
                'description': 'You don\'t have permission to access this resource. This is different from 401 - you are authenticated but not authorized.',
                'solution': 'If you believe you should have access, contact our support team. Otherwise, check if you\'re logged into the correct account.',
                'severity': 'error',
                'is_http_standard': True,
            },
            {
                'code': '404',
                'title': 'Page Not Found',
                'description': 'The requested page or resource was not found on our server. The product may have been discontinued or the URL may be incorrect.',
                'solution': 'Use the search bar to find what you\'re looking for. Check for typos in the URL. Browse our categories to find similar products.',
                'severity': 'warning',
                'is_http_standard': True,
            },
            {
                'code': '429',
                'title': 'Too Many Requests',
                'description': 'You\'ve made too many requests in a short period of time. Our rate limiting is protecting the service.',
                'solution': 'Please wait a few minutes before trying again. If you\'re using an API, implement proper rate limiting in your application.',
                'severity': 'warning',
                'is_http_standard': True,
            },
            {
                'code': '500',
                'title': 'Internal Server Error',
                'description': 'Something went wrong on our server. This is not your fault - it\'s an issue on our end.',
                'solution': 'Please try again in a few minutes. If the problem persists, contact our support team at support@electrostore.in. Your shopping cart data is saved.',
                'severity': 'critical',
                'is_http_standard': True,
            },
            {
                'code': '503',
                'title': 'Service Unavailable',
                'description': 'The server is temporarily unable to handle requests. This usually happens during maintenance or when we\'re experiencing high traffic.',
                'solution': 'Please try again later. Check our status page at status.electrostore.in for updates. Follow @ElectroStore on Twitter for real-time updates.',
                'severity': 'critical',
                'is_http_standard': True,
            },
            {
                'code': 'ES001',
                'title': 'Payment Declined',
                'description': 'Your payment could not be processed. This is an ElectroStore-specific error indicating payment failure.',
                'solution': '1. Check your card details and try again\n2. Ensure sufficient balance in your account\n3. Try a different payment method\n4. Contact your bank if the issue persists\n5. Use UPI for instant payment processing',
                'severity': 'error',
                'is_http_standard': False,
            },
        ]

        created = 0
        for ec_data in error_codes_data:
            _, created_flag = ErrorCode.objects.get_or_create(
                code=ec_data['code'],
                defaults={
                    'title': ec_data['title'],
                    'description': ec_data['description'],
                    'solution': ec_data['solution'],
                    'severity': ec_data['severity'],
                    'is_http_standard': ec_data['is_http_standard'],
                }
            )
            if created_flag:
                created += 1

        self.stdout.write(f'  ✓ Created {created} error codes')
