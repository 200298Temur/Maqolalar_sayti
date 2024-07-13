from django.contrib import admin
from .models import *


@admin.register(Maqola)
class MaqolaAdmin(admin.ModelAdmin):
    fields=['title','slug','content','cat','author',"is_published","rejection"]
    readonly_fields=["time_create","author",]
    list_display=('title',"author",'cat','time_create',"is_published","rejection")
    list_display_links=("title",)
    ordering=("-time_create","title")
    search_fields=('title','cat__name',"author",)
    list_filter=['cat__name','is_published',]
    save_on_top=True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name","author")
    list_display_links = ("id", "name","author")
    prepopulated_fields = {'slug': ('name',)}  # Correcting this part
