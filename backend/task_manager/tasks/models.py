from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    description = models.TextField()

    status = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
<<<<<<< HEAD
        return self.title
=======
        return self.title
>>>>>>> 222f34997776a48e9abd5465f99a1561aa6c82cc
