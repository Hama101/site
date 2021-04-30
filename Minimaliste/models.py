from django.db import models as m
from django.contrib.auth.models import User

from ckeditor.fields import RichTextField
from datetime import date

from PIL import Image
import os


class Profile(m.Model):
    sexe = [
        ("Homme","Homme"),
        ("Femme","Femme"),
    ]
    user = m.OneToOneField(User, verbose_name=("profile"), on_delete=m.CASCADE)
    firstname = m.CharField(max_length=60 ,null=True , blank=True)
    lastname = m.CharField(max_length=60 ,null=True , blank=True )
    birthday = m.DateField(null=True , blank=True)
    image = m.ImageField(null=True , blank=True , upload_to="./profile/images/")
    gender = m.CharField(max_length=20 ,choices=sexe,null=True , blank=True)
    phone = m.CharField(max_length=20 ,null=True , blank=True)
    address = m.CharField(max_length=200 ,null=True , blank=True)
    def __str__(self):
        return self.user.username



    @property
    def avatar(self):
        try:
            return f"https://minimaliste.s3.eu-west-3.amazonaws.com/{self.image}"
        except :
            if self.gender == 'Homme':
                return 'https://bootdey.com/img/Content/avatar/avatar1.png'
            else:
                return 'https://i.pinimg.com/originals/82/ab/35/82ab3533ee71daf256f23c1ccf20ad6f.jpg'


# Create your models here.
class Post(m.Model):
    cats = [
        ('Marketplace' , 'Marketplace'),
        ('Location','Location'),
        ('Services','Services'),
        ('Echange','Echange'),
        ('Object gratuits' , 'Object gratuits')
    ]

    user = m.ForeignKey(User , on_delete=m.CASCADE , null=True , blank=True)
    title = m.CharField(max_length=200 , null=True , blank=True)
    category = m.CharField(max_length=30 , choices=cats , null=True , blank=True)
    sub_category = m.CharField(max_length=60 ,  null=True , blank=True)
    sub_sub = m.CharField(max_length=60 ,  null=True , blank=True)
    cover = m.ImageField(null=True , blank=True ,upload_to="./posts/images/")
    created = m.DateTimeField(auto_now_add=True , null=True , blank=True)
    price = m.FloatField(blank=True , null=True)
    pays = m.CharField(max_length=20 , null=True , blank=True)
    ville = m.CharField(max_length=20 , null=True , blank=True)
    phone = m.CharField(max_length=200,null=True , blank=True)
    shortDescription = m.TextField(max_length=2000,null=True , blank=True)
    description = RichTextField()


    def __str__(self):
        try :
            return self.title
        except :
            return f"object ({self.id})"

    @property
    def imgUrl(self):
        try:
            return f"https://minimaliste.s3.eu-west-3.amazonaws.com/{self.cover}"
        except:
            return ''


class Tag(m.Model):
    name = m.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

class Blog(m.Model):
    title = m.CharField(max_length=1000, null=True, blank=True)
    created = m.DateTimeField(auto_now_add=True , null=True , blank=True)
    shortDescription = m.TextField(blank=True, null=True , max_length=2000)
    body = RichTextField(null=True, blank=True)
    cover = m.ImageField(null=True , blank=True ,upload_to="./blog/images/" )
    tags = m.ManyToManyField(Tag, blank=True , null=True)

    def __str__(self):
        return self.title

    @property
    def imgUrl(self):
        try :
            return f"https://minimaliste.s3.eu-west-3.amazonaws.com/{self.cover}"
        except:
            return ''


class Comment(m.Model):
    user = m.ForeignKey(User , on_delete=m.CASCADE , null=True , blank=True)
    post = m.ForeignKey(Blog ,on_delete=m.CASCADE , null=True , blank=True)
    body = m.TextField(null=True , blank=True)
    commented_at = m.DateTimeField(auto_now_add=True)


class Pro(m.Model):
    user = m.OneToOneField(User , on_delete=m.CASCADE , null=True , blank=True)
    siret = m.CharField(max_length=200 , null=True , blank=True)
    startupName = m.CharField(max_length=200 , null=True , blank=True)
    skills = m.CharField(max_length=200 , null=True , blank=True)
    codePostal = m.CharField(max_length=200 ,null=True , blank=True)
    phone = m.CharField(max_length=255 , null=True , blank=True)
    paid_until = m.DateField(blank=True , null=True)

    @property
    def has_paid(self):
        today = date.today()
        return today < self.paid_until

    def __str__(self):
        try :
            return self.user.get_username()
        except :
            return 'user'


