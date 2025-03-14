from django.db import models
from django.contrib.auth import get_user_model
from jobs.models import Job

User = get_user_model()


class Interview(models.Model):
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    scheduled_at = models.DateTimeField()
    status = models.CharField(max_length=100, choices=[('scheduled', 'Scheduled'), ('completed', 'Completed')])
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.candidate.username} - {self.job.title}"
