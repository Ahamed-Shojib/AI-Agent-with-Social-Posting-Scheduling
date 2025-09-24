from django.shortcuts import render

# Create your views here.
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Customization

def designer_view(request):
    
    designs = Customization.objects.order_by('-created_at')[:5]
    return render(request, 'task_2/index.html', {'designs': designs})

# API endpoint to save a new customization
@require_http_methods(["POST"])
def save_customization(request):
    try:
        data = json.loads(request.body)
        text = data.get('text', '').strip()

        if not text:
            return JsonResponse({'status': 'error', 'message': 'Text cannot be empty.'}, status=400)
        
        Customization.objects.create(custom_text=text)

        # Fetch the latest list of designs to send back to the frontend
        latest_designs = list(Customization.objects.order_by('-created_at')[:5].values('custom_text'))

        return JsonResponse({
            'status': 'success',
            'message': 'Design saved successfully! ',
            'designs': latest_designs
        })
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON.'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)