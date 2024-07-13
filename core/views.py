from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView,CreateView,DetailView,UpdateView
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth import get_user_model
from django import template
from .forms import *

def menufunc(user):
    if user.is_authenticated and user.groups.filter(name='Muharirlar').exists():
        return [
            {"title": "Asosiy Oyna", 'url_name': 'home'},
            {"title": "Maqola qo'shish", 'url_name': 'add_page'},
            {"title": "Sayt haqida", 'url_name': 'about'},
            {"title": "Maqolalarim", 'url_name': 'users:maqolam'},
            {"title": "Muharirlar Kabineti", 'url_name': 'muharir'},
        ]
    else:
        return [
            {"title": "Asosiy Oyna", 'url_name': 'home'},
            {"title": "Maqola qo'shish", 'url_name': 'add_page'},
            {"title": "Sayt haqida", 'url_name': 'about'},
            {"title": "Maqolalarim", 'url_name': 'users:maqolam'}
        ]

class GroupRequiredMixin(UserPassesTestMixin):
    group_name = 'Muharirlar'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.groups.filter(name=self.group_name).exists()

    def handle_no_permission(self):
        from django.shortcuts import redirect
        return redirect('no_permission')  

class About(ListView):
    model=Maqola.objects.all()
    template_name="core/about.html"
    title_page='About'
    paginate_by=3
    post=Maqola.objects.all()
    context_object_name='posts'
    extra_context={
        'post':post,
        'cat_selected':0
    }
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menufunc(self.request.user)
        return context

    
    def  get_queryset(self):
        return Maqola.objects.filter(is_published=True).select_related("cat")


def get_categories():
    categories = Category.objects.all()
    cats_db = [{'id': cat.id, 'name': cat.name} for cat in categories]
    return cats_db


class AddPage(UserPassesTestMixin,CreateView):
    form_class=AddPageForm
    template_name="core/addpage.html"
    success_url=reverse_lazy("home")
    title_page="Maqola Qo'shish"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menufunc(self.request.user)
        return context
    def test_func(self):
            return self.request.user.is_authenticated

    def form_valid(self, form):
        w=form.save(commit=False)
        w.author=self.request.user
        return super().form_valid(form)



class Home(ListView):
    
    model=Maqola.objects.all().filter()
    context_object_name = 'posts'
    paginate_by=3
    template_name='core/home.html'
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menufunc(self.request.user)
        context['title'] = "Asosiy Oyna"
        context['cat_selected'] = 0
        return context

    def  get_queryset(self):
        return Maqola.objects.filter(is_published=True) 

class CategoryView(ListView):
    model = Maqola
    template_name = 'core/index.html'
    context_object_name = 'posts'
    paginate_by=3
    # paginate_by = 10  # Add pagination if needed

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['cat_slug'])
        return Maqola.objects.filter(cat_id=self.category.pk,is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.category.name
        context['menu'] = menufunc(self.request.user)
        context['cat_selected'] = self.category.slug  # Use 'slug' if that's the identifier
        return context   


def show_post(request, post_slug):
    post = get_object_or_404(Maqola, slug=post_slug)
    
    data = {
        'title': post.title,
        'menu': menufunc(request.user),
        'post': post,
        'cat_selected': 1, 
    }
    return render(request, "core/post.html", data)

def show_post_update(request, post_update_slug):
    post = get_object_or_404(Maqola, slug=post_update_slug)
    
    data = {
        'title': post.title,
        'menu': menufunc(request.user),
        'post': post,
        'cat_selected': 1, 
    }
    return render(request, "core/post_update.html", data)

def no_permission_view(request):
    return render(request, 'core/no_permission.html')

class MuharrirKabinet(GroupRequiredMixin,ListView):
    model=Maqola
    template_name="core/maqolalar.html"
    context_object_name = 'posts'
    paginate_by=3
    extra_context={
        'title':"Maqolalar",
        'cat_selected':0,
    }
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menufunc(self.request.user)
        return context

    def get_queryset(self):
        user = self.request.user
        return Maqola.objects.filter(cat__author=user)
    
class AuthorView(ListView):
    model = Maqola
    template_name = 'core/maqolalar.html'
    context_object_name = 'posts'
    paginate_by = 3  # Add pagination if needed

    def get_queryset(self):
        return Maqola.objects.filter(author__id=self.kwargs['author_id'],cat__author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # author_id ni oling
        author_id = self.kwargs.get('author_id')
        author = get_user_model().objects.get(id=author_id)
        
        context['title'] = f"{author.username} maqolalari"  # author.name o'rniga author.username
        context['menu'] = menufunc(self.request.user)
        context['cat_selected'] = author_id  # author_id ni category_selected ga o'rnatish

        return context

class AuthorViewMain(ListView):
    model = Maqola
    paginate_by=3
    template_name = 'core/home.html'
    context_object_name = 'posts'
    

    def get_queryset(self):
        author_id = self.kwargs.get('author_id')
        user = self.request.user
        
        if author_id is not None:
            return Maqola.objects.filter(author__id=author_id, is_published=True)
        else:
            return Maqola.objects.none()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        author_id = self.kwargs.get('author_id')
        author = get_object_or_404(get_user_model(), id=author_id)
        
        context['title'] = f"{author.username} maqolalari"  # author.name o'rniga author.username
        context['menu'] = menufunc(self.request.user)
        context['cat_selected'] = author_id  # author_id ni category_selected ga o'rnatish

        return context

class UpdatePage(UpdateView):
    form_class = UpdateForm
    template_name = 'core/updatepage.html'
    success_url = reverse_lazy('muharir')
    
    def get_queryset(self):
        return Maqola.objects.all()  # Yoki kerakli querysetni aniqlang
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menufunc(self.request.user)
        context['title'] = 'Maqolani tekshirish'
        return context
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        if instance.is_published:
            instance.rejection = False
        else:
            instance.rejection = True
        instance.save()
        return super().form_valid(form)