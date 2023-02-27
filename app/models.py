from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
User = get_user_model()
from versatileimagefield.fields import VersatileImageField

from django.contrib.humanize.templatetags import humanize
class Post(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	text = models.TextField(blank=True, null=True)
	time_creation = models.DateTimeField(auto_now_add=True,null=True)


	def __str__(self):
		return str(self.id)

	def get_likes_amount(self):
		return self.like_set.all().count()

	def get_comments_amount(self):
		return self.comment_set.all().count()

	def get_shares_amount(self):
		return self.share_set.all().count()

	def get_natural_time(self):
		return humanize.naturaltime(self.time_creation)

	def get_natural_day(self):
		return humanize.naturalday(self.time_creation)


from .helpers import get_random_alphanumeric_string
def get_upload_path(instance,filename):
	ext = filename.split('.')[-1]
	randomfilename = get_random_alphanumeric_string(20)
	resultfilename = "%s.%s" % (randomfilename, ext)
	return 'user/{}/post/{}/{}'.format(instance.post.user.id,instance.post.id,resultfilename)

from django.core.exceptions import ValidationError

def file_size(value): # add this to some file where you can import it from
    limit = 8 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 8 MiB.')
    
class PostMedia(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	image = VersatileImageField(blank=True,null=True,upload_to=get_upload_path,validators=[file_size])
	time_creation = models.DateTimeField(auto_now_add=True,null=True,blank=True)
	
	def __str__(self):
		return str(self.id)


class Save(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	post = models.ForeignKey(Post,on_delete=models.CASCADE)

	def __str__(self):
		return str(self.id)

class Share(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.id)



class Comment(models.Model):
	post = models.ForeignKey(Post,on_delete=models.CASCADE)
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	text = models.TextField(blank=True, null=True)
	time_creation = models.DateTimeField(auto_now_add=True,null=True)

	def __str__(self):
		return str(self.id)

	def get_likes_amount(self):
		return self.like_set.all().count()

	def get_replies_amount(self):
		return self.reply_set.all().count()

	def get_natural_time(self):
		return humanize.naturaltime(self.time_creation)

	def get_natural_day(self):
		return humanize.naturalday(self.time_creation)

class Reply(models.Model):
	comment = models.ForeignKey(Comment,on_delete=models.CASCADE)
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	text = models.TextField(blank=True, null=True)
	time_creation = models.DateTimeField(auto_now_add=True,null=True)

	def __str__(self):
		return str(self.id)

	def get_likes_amount(self):
		return self.like_set.all().count()

	def get_natural_time(self):
		return humanize.naturaltime(self.time_creation)

	def get_natural_day(self):
		return humanize.naturalday(self.time_creation)

class Report(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	to_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="reported",null=True,blank=True)
	to_post = models.ForeignKey(Post, on_delete=models.CASCADE,null=True,blank=True)
	to_comment = models.ForeignKey(Comment, on_delete=models.CASCADE,null=True,blank=True)
	to_reply = models.ForeignKey(Reply, on_delete=models.CASCADE,null=True,blank=True)

	def __str__(self):
		return str(self.id)

class Like(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post,on_delete=models.CASCADE, null=True,blank=True)
	comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True,blank=True)
	reply = models.ForeignKey(Reply, on_delete=models.CASCADE, null=True,blank=True)
	time_creation = models.DateTimeField(auto_now_add=True,null=True)

	def __str__(self):
		return str(self.id)
	
	def get_natural_time(self):
		return humanize.naturaltime(self.time_creation)

	def get_natural_day(self):
		return humanize.naturalday(self.time_creation)