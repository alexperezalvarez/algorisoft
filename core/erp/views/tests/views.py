from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from core.erp.forms import TestForm
from core.erp.models import Category, Product

class TestView(TemplateView):
    template_name='tests.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required) 
    def dispatch(self, request, *args,**kwargs):
     return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
      data={}
      try:
        action = request.POST['action']
        if action == 'search_product_id':
          data=[{"id":'','text':'-'*9}] #como le ponia el primero como rayitas en el html porque no era nada, pero ahora recibe el data desde aqui entonces debo pasarle esa seleccion desde aca, sin id y pues los guiones
          for i in Product.objects.filter(cat_id=request.POST['id']):
             #le paso otro valor data a los productos segun la categoria, y hasta en el data puedo pasarle valores que necesite en el front, en este caso la info de la categoria del producto
             data.append({'id':i.id, 'text':i.name,'data':i.cat.toJSON()}) 
             #porque asi lo pide el select2 para pasarle los datos
        if action=="autocomplete":
           data=[]
           # le envio unos 10 registros nada más para no mandarle todo y se vuelva pesado
           for i in Category.objects.filter(name__icontains=request.POST['term'])[0:10]:
              item=i.toJSON()
              # le agrego la clave value porque la necesita el autocomplete
              item['value']=i.name
              data.append(item)
        else:
          data['error']='Ha ocurrido un error'
      except Exception as e:
         data={}
         data['error']=str(e)
         #recordar que como voy a retornar un arreglo o coleccion, el JsonResponse debe tener el safe en False
      return JsonResponse(data,safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Selects anidados | Django'
        context['form']=TestForm()
        return context
    