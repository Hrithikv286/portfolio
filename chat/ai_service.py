"""
AI Assistant service using Google Gemini API
Answers FAQs, explains error codes, and creates support tickets
"""
import logging
import re
from django.conf import settings
from store.models import FAQ, ErrorCode, SupportTicket

logger = logging.getLogger('chat')

# System prompt for the AI assistant
SYSTEM_PROMPT = """You are ElectroBot, the helpful AI assistant for ElectroStore - a premium electronics e-commerce platform.

Your responsibilities:
1. Answer questions about products, orders, shipping, returns, and warranties
2. Explain HTTP error codes and site-specific error codes in simple terms
3. Help customers with account and payment issues
4. Be friendly, professional, and concise

Store Information:
- We sell smartphones, laptops, TVs, audio devices, gaming gear, smart home devices, and accessories
- Free shipping on orders above ₹999
- 7-day return policy for most products
- 1-year manufacturer warranty on all electronics
- We accept UPI, credit/debit cards, net banking, and EMI options
- Customer support: support@electrostore.in | +91-1800-123-4567

Guidelines:
- Keep responses under 200 words
- Be empathetic and helpful
- If you cannot answer, acknowledge it and tell the customer a ticket will be created
- For error codes, explain what they mean and how to resolve them
- Format responses with proper structure when listing items

Respond ONLY in English."""


def get_gemini_response(user_message, context_faqs=None, context_errors=None):
    """Get response from Google Gemini API"""
    api_key = settings.GEMINI_API_KEY

    if not api_key:
        logger.warning("GEMINI_API_KEY not configured")
        return None, "api_not_configured"

    try:
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Build context
        context_parts = [SYSTEM_PROMPT]

        if context_faqs:
            faq_text = "\n\nRelevant FAQ answers:\n"
            for faq in context_faqs[:3]:
                faq_text += f"Q: {faq.question}\nA: {faq.answer}\n\n"
            context_parts.append(faq_text)

        if context_errors:
            error_text = "\n\nRelevant Error Code information:\n"
            for error in context_errors[:2]:
                error_text += f"Error {error.code} ({error.title}): {error.description}\nSolution: {error.solution}\n\n"
            context_parts.append(error_text)

        full_prompt = "\n".join(context_parts) + f"\n\nUser question: {user_message}"

        response = model.generate_content(full_prompt)
        return response.text, "success"

    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        return None, str(e)


def get_faq_matches(user_message):
    """Find relevant FAQs using keyword matching"""
    from django.db.models import Q

    # Extract keywords (simple approach)
    words = re.findall(r'\b\w{4,}\b', user_message.lower())
    if not words:
        return FAQ.objects.none()

    query = Q()
    for word in words[:5]:  # Limit to first 5 keywords
        query |= Q(question__icontains=word) | Q(answer__icontains=word)

    return FAQ.objects.filter(query, is_active=True)[:3]


def get_error_matches(user_message):
    """Find relevant error codes mentioned in the message"""
    # Look for error codes like 404, 500, ES001 (case-insensitive)
    error_pattern = re.compile(r'\b(es\d+|\d{3})\b', re.IGNORECASE)
    matches = [m.upper() for m in error_pattern.findall(user_message)]

    if matches:
        return ErrorCode.objects.filter(code__in=matches)
    return ErrorCode.objects.none()


def process_chat_message(user_message, session_id):
    """
    Main chat processing function:
    1. Find relevant FAQs
    2. Find relevant error codes
    3. Query Gemini with context
    4. If Gemini fails, use rule-based fallback
    5. Create support ticket if cannot answer
    """
    user_message = user_message.strip()
    if not user_message:
        return {
            'response': "Please type a message to get started! 😊",
            'ticket_created': False,
            'ticket_id': None,
            'source': 'validation',
        }

    # Find relevant FAQs and error codes for context
    context_faqs = list(get_faq_matches(user_message))
    context_errors = list(get_error_matches(user_message))

    # Try Gemini AI first
    ai_response, status = get_gemini_response(user_message, context_faqs, context_errors)

    if ai_response and status == "success":
        return {
            'response': ai_response,
            'ticket_created': False,
            'ticket_id': None,
            'source': 'gemini',
        }

    # Error code fallback - prioritize when an error code is detected
    if context_errors:
        error = context_errors[0]
        error_response = (
            f"**Error {error.code}: {error.title}**\n\n"
            f"{error.description}\n\n"
            f"**How to fix:**\n{error.solution}"
        )
        return {
            'response': error_response,
            'ticket_created': False,
            'ticket_id': None,
            'source': 'error_fallback',
        }

    # Fallback: Rule-based responses using FAQ data
    if context_faqs:
        faq_response = f"Based on our FAQs, here's what I found:\n\n"
        for faq in context_faqs[:2]:
            faq_response += f"**{faq.question}**\n{faq.answer}\n\n"
        return {
            'response': faq_response,
            'ticket_created': False,
            'ticket_id': None,
            'source': 'faq_fallback',
        }

    # Cannot answer - create a support ticket
    try:
        ticket = SupportTicket.objects.create(
            user_message=user_message,
            session_id=session_id,
            priority='medium',
        )
        response = (
            f"I'm sorry, I couldn't find a specific answer to your question. "
            f"I've created a support ticket (#{ticket.ticket_id}) for you. "
            f"Our team will get back to you within 24 hours. "
            f"You can also reach us at support@electrostore.in or call +91-1800-123-4567."
        )
        return {
            'response': response,
            'ticket_created': True,
            'ticket_id': ticket.ticket_id,
            'source': 'ticket_created',
        }
    except Exception as e:
        logger.error(f"Failed to create support ticket: {e}")
        return {
            'response': "I'm having trouble right now. Please contact our support at support@electrostore.in",
            'ticket_created': False,
            'ticket_id': None,
            'source': 'error',
        }
