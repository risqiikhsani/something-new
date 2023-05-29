from django.db import models
from versatileimagefield.fields import VersatileImageField
from django.conf import settings
User = settings.AUTH_USER_MODEL

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# class Ingredient(models.Model):
#     name = models.CharField(max_length=100)
#     notes = models.TextField()
#     category = models.ForeignKey(
#         Category, related_name="ingredients", on_delete=models.CASCADE
#     )

#     def __str__(self):
#         return self.name
    

class Item(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    detail = models.TextField()
    price = models.FloatField(default=0,blank=True,null=True)
    amount = models.IntegerField(blank=True,null=True,default=1)
    used_condition = models.BooleanField(default=False,null=True,blank=True)
    sold = models.BooleanField(default=False,null=True,blank=True)
    active = models.BooleanField(default=True, null=True,blank=True)

    def __str__(self):
        return self.name
    

from .helpers import get_random_alphanumeric_string
def get_upload_path(instance,filename):
	ext = filename.split('.')[-1]
	randomfilename = get_random_alphanumeric_string(20)
	resultfilename = "%s.%s" % (randomfilename, ext)
	return 'user/{}/item/{}/photos/{}'.format(instance.item.user.id,instance.item.id,resultfilename)

from django.core.exceptions import ValidationError

def file_size(value): # add this to some file where you can import it from
    limit = 8 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 8 MiB.')
    
class Photo(models.Model):
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    photo = VersatileImageField(
        upload_to=get_upload_path,
		validators=[file_size],
		null=True,
		blank=True
    )
    is_background = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.id)
    
