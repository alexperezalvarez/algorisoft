from django.http import JsonResponse
from django.urls import reverse_lazy
from core.erp.models import *
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,FormView
from django.views.decorators.csrf import csrf_exempt
from core.erp.forms import *
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

#es mejor trabajar con las vistas pq al trabajar con funciones, es dificil hacer mantenimiento y más cuando se trabaja con los metodos post, get etc, para eso, las clases ya tiene una forma mas ordenada y limpia para trabajar

# def category_list(request):
#     data={
#         'title':'Listado de Categorias',
#         'categories':Category.objects.all()
#     }
#     return render(request, 'category/list.html',data)

class CategoryListView(ListView):
  model = Category
  #el objecto que tiene las categorias se llama object_list
  template_name= 'category/list.html'

  #esto es un metodo decorador, que po ejemplo puedo hacer una verificacion antes de ejecutar el dispatch u otra funcion, en este caso, no lo dejo entrar a la pagina (GET) hasta que este logueado
  #@method_decorator(login_required)
  #con este decorador, le quito la proteccion solo en esta vista, para el metodo post, y va aqui pq el dispatch es el que recibe los metodos del request
  @method_decorator(csrf_exempt)
  @method_decorator(login_required) #para que no lo deje entrar a la vista hasta que este registrado, utiliza la variable LOGIN_URL del settings.py, lo pongo en todas mis vistas en el metodo dispatch
  def dispatch(self, request, *args,**kwargs):
     #esta funcion maneja como llegan los metodos de las peticiones
    #  if request.method == 'GET':
    #     return redirect('erp:category_list2')
     return super().dispatch(request, *args, **kwargs)
  
  #puedo editar el metodo post, cuando hago una peticion sin el codigo de seguridad, tirara error
  def post(self, request, *args, **kwargs):
    try:
      #data = Category.objects.get(pk=request.POST['id']).toJSON()
      #obtengo la acción
      action = request.POST['action']
      if action == 'searchdata':
        #un arreglo pq asi los recibe datatable
        data = []
        for i in Category.objects.all():
          #lo convertimos a diccionario con la función que creamos
          data.append(i.toJSON())
      else:
        data['error']='Ha ocurrido un error'
    except Exception as e:
       data['error']=str(e)
    #por defecto, safe siempre esta en True para serializar los datos a json, pero un arreglo no se puede serializar a json, entonces como le vamos a pasar un arreglo, le ponemos el safe como False para poner enviar
    return JsonResponse(data,safe=False)

  def get_queryset(self):
     #esta funcion es la que hace la consulta la cual se guarda en el object_list, puedo modificarla tambien
     #puedo hasta aplicar filtros para mostrar
     #return Category.objects.filter(name__startswith='B')
     return Category.objects.all()

  def get_context_data(self, **kwargs):
    #con super traigo los datos que ya tiene la clase y agrego lo que quiera
    context = super().get_context_data(**kwargs)
    context['title']='Listado de Categorias'
    #como tengo una plantilla para las listas, le paso la ruta a donde va a ir el boton
    context['create_url']=reverse_lazy('erp:category_create')
    context['entity']='Categorias'
    context['list_url']=reverse_lazy('erp:category_list')
    #puedo modificar esa clave la cual tiene el object_list
    #context['object_list'] = Product.objects.all()
    return context

class CategoryCreateView(CreateView):
  model = Category
  form_class = CategoryForm
  template_name = 'category/create.html'
  #reverse_lazy retorna la ruta que le pase por en name de las rutas y ponerla en esa variable
  success_url = reverse_lazy('erp:category_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
      return super().dispatch(request, *args, **kwargs)
  

  def post(self, request,*args, **kwargs):
    data = {}
    try:
      action=request.POST['action']
      if action=='add':
        # form=CategoryForm(request.POST)
        #asi es lo mismo que arriba, pero es mejor, en tal caso que se envien archivos, eso va en el request.FILES pero con el self.get_form() obtengo todo el formulario
        form=self.get_form()
        #ahi ya sobreescribi el metodo save
        data = form.save()
        # if form.is_valid():
        #   form.save()
        # else:
        #   data['error']=form.errors
      else:
        data['error']='No ha ingresado a ninguna opción'
    except Exception as e:
       data['error']=str(e)
       
    return JsonResponse(data)
  

  #   print(request.POST)
  #   form=CategoryForm(request.POST)
  #   if form.is_valid():
  #      form.save()
  #      return HttpResponseRedirect(self.success_url)
  #   #esto lo pongo, pq cuando no hay errores, esta variable debe ser None
  #   self.object = None
  #   #con esto traigo los valores que ya tiene, en este caso, el titulo, sino lo llamo no utilizara el title que le tengo en la funcion
  #   context = self.get_context_data(**kwargs)
  #   context['form']=form
  #   return render(request, self.template_name,context)
  # # esta es la forma en como trabaja el post, pero no es necesario hacerlo, nomas se hizo a modo de explicacion
  def get_context_data(self, **kwargs):
     context = super().get_context_data(**kwargs)
     context['title']='Creación de una categoria'
     context['entity']='Categorias'
     context['m_confirm']='la categoria'
     context['list_url']=reverse_lazy('erp:category_list')
     #para saber que accion va a realizar al post
     context['action']='add'
     return context

class CategoryUpdateView(UpdateView):
  #lo que hace el updateview, obtiene los valores pasandole los valores del post y creando una instacia para obtener los valores del objeto, la cual se guardan en el self.object
  model = Category
  form_class = CategoryForm
  template_name = 'category/create.html'
  success_url = reverse_lazy('erp:category_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    #asi ya el post trabaja para actualizar el objeto, porque con el get_object() obtengo el objeto a modificar, y asi el get_form ya no seria un tipo "CategoryForm(request.POST)" sino que crea la instancia y deja actualizar "CategoryForm(request.POST,instance=self.object)"
    self.object = self.get_object()
    return super().dispatch(request, *args, **kwargs)

  def post(self, request,*args, **kwargs):
    data = {}
    try:
      action=request.POST['action']
      if action=='edit':
        #si lo dejo asi, el formulario lanzaria un error pq esta intentando crear un objeto en vez de actualizarlo, porque el self.object estaria en None
        form=self.get_form()
        data = form.save()
      else:
        data['error']='No ha ingresado a ninguna opción'
    except Exception as e:
       data['error']=str(e)
       
    return JsonResponse(data)

  def get_context_data(self, **kwargs):
     context = super().get_context_data(**kwargs)
     context['title']='Edición de una categoria'
     context['entity']='Categorias'
     context['m_confirm']='la categoria'
     context['list_url']=reverse_lazy('erp:category_list')
     #para saber que accion va a realizar al post
     context['action']='edit'
     return context

class CategoryDeleteView(DeleteView):
  model = Category
  template_name = 'category/delete.html'
  success_url = reverse_lazy('erp:category_list')

  @method_decorator(login_required)
  def dispatch(self,request, *args, **kwargs):
    self.object = self.get_object()
    return super().dispatch(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    data = {}
    try:
      #cuando sobre escribo el post, el self.object que tiene la instacia, queda vacio, asi que modifico el dispatch para capturar la instacia
      #ya como tengo la instancia (gracias al distpach), osea el CategoryForm(request, instance=self.object), ya puedo aplicar su funcion .delete()
      self.object.delete()
    except Exception as e:
      data['error']=str(e)
    return JsonResponse(data)

  def get_context_data(self, **kwargs):
     context = super().get_context_data(**kwargs)
     context['title']='Eliminación de una categoria'
     context['entity']='Categorias'
     context['list_url']=reverse_lazy('erp:category_list')
     return context

#esta vista es para trabajar con un formulario cualquiera, en este caso hare como si fuera para crear una categoria, lo mismo que la otra clase pero la diferencia es que la otra es especificamente para crear un registro
class CategoryFormView(FormView):
  #por ahora no va a guardar nada, pero si va a verificar las validaciones que tenga
  form_class = CategoryForm
  #utilizo el mismo template para la creación
  template_name = 'category/create.html'
  success_url = reverse_lazy('erp:category_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
      return super().dispatch(request, *args, **kwargs)
  

  def form_invalid(self, form):
    #aqui veo los errores que tenga el formulario
    print(form.errors)
    print(form.is_valid()) #esto retornaria false porque el form no es valido
    return super().form_invalid(form)

  def form_valid(self, form):
    #este es cuando el formulario es valido

    #me lanzara true pq si es valido por eso entra a esta función
    print(form.is_valid())
    print(form)
    #si quiero guardar el registro con esta vista, ya aqui en la funcion de form_valid, agrego las lineas correspondientes (form.save())
    return super().form_valid(form)

  def get_context_data(self, **kwargs):
     context = super().get_context_data(**kwargs)
     #le pongo una pleca para diferenciarlo
     context['title']='Form | Creación de una categoria'
     context['entity']='Categorias'
     context['list_url']=reverse_lazy('erp:category_list')
     #para saber que accion va a realizar al post
     context['action']='add'
     return context
