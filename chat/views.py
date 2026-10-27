"""
Chat app views - AI Assistant API endpoints
"""
import json
import uuid
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .ai_service import process_chat_message
from .mongo_client import save_chat_log, save_feedback

logger = logging.getLogger('chat')


def get_or_create_session(request):
    """Get or create a session ID for the user"""
    if 'chat_session_id' not in request.session:
        request.session['chat_session_id'] = str(uuid.uuid4())
    return request.session['chat_session_id']


@csrf_exempt
@require_http_methods(['POST'])
def send_message(request):
    """Handle chat messages from the AI assistant widget"""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()

        if not user_message:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)

        if len(user_message) > 1000:
            return JsonResponse({'error': 'Message too long (max 1000 characters)'}, status=400)

        session_id = get_or_create_session(request)

        # Process message through AI service
        result = process_chat_message(user_message, session_id)

        # Save to MongoDB
        log_id = save_chat_log(
            session_id=session_id,
            user_message=user_message,
            bot_response=result['response'],
        )

        return JsonResponse({
            'success': True,
            'response': result['response'],
            'ticket_created': result.get('ticket_created', False),
            'ticket_id': result.get('ticket_id'),
            'log_id': log_id,
            'source': result.get('source', 'unknown'),
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return JsonResponse({'error': 'Internal server error'}, status=500)


@csrf_exempt
@require_http_methods(['POST'])
def submit_feedback(request):
    """Submit feedback for a chat interaction"""
    try:
        data = json.loads(request.body)
        log_id = data.get('log_id', '')
        rating = data.get('rating', 0)
        comment = data.get('comment', '')

        if not log_id:
            return JsonResponse({'error': 'log_id is required'}, status=400)

        if rating not in [1, 2, 3, 4, 5]:
            return JsonResponse({'error': 'Rating must be between 1-5'}, status=400)

        success = save_feedback(log_id, rating, comment)

        return JsonResponse({'success': success})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error(f"Feedback error: {e}")
        return JsonResponse({'error': 'Internal server error'}, status=500)


@require_http_methods(['GET'])
def get_suggestions(request):
    """Get suggested questions for the chat widget"""
    suggestions = [
        "How do I track my order?",
        "What is the return policy?",
        "How long does delivery take?",
        "What payment methods do you accept?",
        "How do I reset my password?",
        "What does error 404 mean?",
        "Is there a warranty on products?",
        "How do I cancel my order?",
    ]
    return JsonResponse({'suggestions': suggestions})
