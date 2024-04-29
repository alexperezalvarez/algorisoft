from django.views.generic import TemplateView

#simplemente un template para una vista normal
class IndexView(TemplateView):
    template_name = 'index.html'