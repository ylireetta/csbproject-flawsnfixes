from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Move(models.Model):
    move_name = models.CharField(max_length=100)

    # basically toString method
    def __str__(self):
        return self.move_name
    
    class Meta:
        db_table = 'movestable'

class Session(models.Model):
    date = models.DateField(default=datetime.now())
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    ended = models.BooleanField(default=True)

    def __str__(self):
        return f'Training session {self.date} for user {self.owner.pk}'
    
    class Meta:
        db_table = 'sessionstable'

class Set(models.Model):
    move_id = models.ForeignKey(Move, on_delete=models.CASCADE)
    reps = models.IntegerField()
    weight = models.IntegerField()
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.reps} * {self.weight} of move id {self.move_id}'

    class Meta:
        db_table = 'setstable'