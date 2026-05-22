from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=255,unique=True)
    def __str__(self):
        return self.name
class Messages(models.Model):
    content = models.JSONField()
    time_stamp = models.DateTimeField(auto_now_add=True)
    REACTION_CHOICES = [
        ("😂","Laugh"),
        ("😭","Cry"),
        ("🎉","Celebrate"),
        ("👀","Eyes"),
        ("😎","Cool"),
        ("😘","Kiss"),
        ("❤","Heart"),
    ]
    reaction = models.CharField(max_length=10,choices=REACTION_CHOICES,null=True,blank=True)
    username = models.CharField(max_length=255)
    room=models.ForeignKey(Room,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.username} : {self.content} ({self.time_stamp})" 