from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

def cover_upload(instance, filename):
    # per-user folder: covers/<author_id>/<filename>
    return f"covers//{instance.author_id}/{filename}"

class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    cover = models.ImageField(upload_to=cover_upload, blank=True, null=True)
    cover_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
    
    def make_unique_slug(self):
        base = slugify(self.title) or "post"
        slug = base
        n = 2
        while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base}--{n}"
            n += 1
        return slug
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.make_unique_slug()
        super().save(*args, **kwargs)

    @property
    def cover_src(self):
        if self.cover:
            return self.cover.url
        return self.cover.url or ""

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="avatars/%Y/%m/", blank=True, null=True)
    bio = models.CharField(max_length=280, blank=True)

    def __str__(self):
        return f"Profile({self.user.username})"
    

@receiver
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)