from django.shortcuts import render
from django.views.generic import ListView
from .models import SaaSTemplate, TemplateCategory

class TemplateListView(ListView):
    model = SaaSTemplate
    template_name = 'templates_catalog/template_list.html'
    context_object_name = 'templates'
    def get_template_names(self):
        if self.request.headers.get('HX-Request'):
            return ['templates_catalog/includes/template_grid_items.html']
        return [self.template_name]

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True)
        category_slug = self.request.GET.get('category')
        search_query = self.request.GET.get('q')

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = TemplateCategory.objects.all()
        context['current_category'] = self.request.GET.get('category', '')
        return context

def template_detail(request, slug):
    template = SaaSTemplate.objects.get(slug=slug, is_active=True)
    return render(request, 'templates_catalog/template_detail.html', {
        'template': template
    })
