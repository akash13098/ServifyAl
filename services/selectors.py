from .models import ServiceCategory

def get_all_categories():
    return ServiceCategory.objects.all()