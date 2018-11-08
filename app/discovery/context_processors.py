from django.conf import settings


def api_host(request):
    return { 
        "API_HOST": settings.API_HOST
    }

def google_analytics(request):
    return { 
        "GA_TRACKING_ID": settings.GA_TRACKING_ID 
    }