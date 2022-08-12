from .models import Category


def related(request):
    context = {
        'category_list': Category.objects.all(),
    }
    return context
