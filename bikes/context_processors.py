from .models import Footer

def footer_context(request):
    footer = Footer.objects.first()
    return {"footer": footer}