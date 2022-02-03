from django.db import models
from slugify import slugify
from django.contrib.auth.models import User
def image_upload(instance,filename):
    (image_names,extension) = (filename.split('.'))
    return f'jobs/{instance.id}.{extension}'

class job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    job_type_choices = (
        ('Full time', 'Full time'),
        ('Part time', 'Part time')
    )
    job_type = models.CharField(max_length=15, choices=job_type_choices)
    description = models.TextField(max_length=500)
    publish_at = models.DateTimeField(auto_now=True)
    salary = models.IntegerField(default=1200)
    vacancy = models.IntegerField(default= 1)
    experince = models.IntegerField(default= 0)
    categorie = models.ForeignKey("categorie", on_delete=models.CASCADE)
    image = models.ImageField( upload_to= image_upload, height_field=None, width_field=None, max_length=None)
    slug = models.SlugField(null=True,blank=True,unique=True)
    def __str__(self) -> str:
        return self.title

    def save(self,*args, **kwargs):
        self.slug = slugify(self.title,to_lower=True)
        super(job,self).save(*args, **kwargs)
    


class categorie(models.Model):
    categorie = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.categorie

class apply_job(models.Model):
    job = models.ForeignKey('job', on_delete=models.CASCADE)
    name = models.CharField( max_length=50)
    email = models.EmailField(max_length=254)
    website = models.URLField(max_length=200)
    cv = models.FileField(upload_to='cv', max_length=100)
    coverletter = models.TextField(max_length=200)

    def __str__(self) -> str:
        return self.name


