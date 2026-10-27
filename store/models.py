"""
Store app models - Products, Categories, FAQs, SupportTickets, ErrorCodes
All stored in SQLite via Django ORM
"""
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='fa-microchip', help_text='Font Awesome icon class')
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    review_count = models.PositiveIntegerField(default=0)
    specifications = models.JSONField(default=dict, blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    image_url = models.URLField(blank=True, help_text='External image URL')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def discount_percentage(self):
        if self.original_price and self.original_price > self.price:
            return int(((self.original_price - self.price) / self.original_price) * 100)
        return 0

    @property
    def is_in_stock(self):
        return self.stock > 0

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        elif self.image_url:
            return self.image_url
        return '/static/images/no-image.png'

    def __str__(self):
        return self.name


class FAQ(models.Model):
    """Frequently Asked Questions - stored in SQL"""
    CATEGORY_CHOICES = [
        ('ordering', 'Ordering & Payment'),
        ('shipping', 'Shipping & Delivery'),
        ('returns', 'Returns & Refunds'),
        ('product', 'Product & Technical'),
        ('account', 'Account & Security'),
        ('warranty', 'Warranty & Support'),
        ('general', 'General'),
    ]

    question = models.CharField(max_length=500)
    answer = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='general')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'FAQ'

    def __str__(self):
        return self.question[:80]


class ErrorCode(models.Model):
    """HTTP Error codes with descriptions - stored in SQL"""
    code = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    solution = models.TextField()
    severity = models.CharField(
        max_length=20,
        choices=[('info', 'Info'), ('warning', 'Warning'), ('error', 'Error'), ('critical', 'Critical')],
        default='error'
    )
    is_http_standard = models.BooleanField(default=True)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.title}"


class SupportTicket(models.Model):
    """Support tickets created by AI when it cannot answer - stored in SQL"""
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    ticket_id = models.CharField(max_length=20, unique=True, blank=True)
    user_message = models.TextField()
    user_email = models.EmailField(blank=True)
    user_name = models.CharField(max_length=100, blank=True)
    session_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    agent_response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.ticket_id:
            import random
            import string
            self.ticket_id = 'ES-' + ''.join(random.choices(string.digits, k=6))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Ticket {self.ticket_id} - {self.status}"
