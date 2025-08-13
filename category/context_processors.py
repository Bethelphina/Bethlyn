from .models import Category

def category_menu_links(request):
    category_obj_items_as_links = Category.objects.all()
    return dict(links=category_obj_items_as_links)