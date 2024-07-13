from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.urls import reverse
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Katigoriya")
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Muharir")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Katigoriya'
        verbose_name_plural = 'Katigoriya'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.id})


class Maqola(models.Model):
    title = models.CharField(max_length=100, verbose_name="Title")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Slug",
                            validators=[
                                MinLengthValidator(3, message="Min simvol 3"),
                                MaxLengthValidator(100, message="Max simvol 100")
                            ])
    content = models.TextField(verbose_name="Content")
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='posts', null=True, default=None)
    is_published = models.BooleanField(default=False, verbose_name="Ruxsat")
    rejection=models.BooleanField(default=False,verbose_name="Rad etish")
    message=models.TextField(null=True,verbose_name="Message",)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqti")
    time_update = models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan vaqti")
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts', verbose_name="Katigoriya")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Maqola"
        verbose_name_plural = "Maqolalar"
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self):
        return reverse("post", kwargs={"post_slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
