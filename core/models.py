from django.db import models


class Booking(models.Model):
    """Booking for a Teams consultation call."""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    project_description = models.TextField(blank=True)
    slot_datetime = models.DateTimeField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)

    class Meta:
        ordering = ['slot_datetime']

    def __str__(self):
        return f"{self.name} — {self.slot_datetime:%a %d %b %H:%M}"
