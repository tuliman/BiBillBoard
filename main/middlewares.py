from .models import SubRubric


def bboard_context_processor(request):
    context = {'rubrics': SubRubric.objects.all()}
    return context
