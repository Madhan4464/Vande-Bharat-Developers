from django.conf import settings


def company_details(request):
    return {
        "company_phone": settings.COMPANY_PHONE,
        "company_email": settings.COMPANY_EMAIL,
        "company_address": settings.COMPANY_ADDRESS,
        "company_whatsapp_number": settings.COMPANY_WHATSAPP_NUMBER,
        "company_map_query": settings.COMPANY_MAP_QUERY,
    }
