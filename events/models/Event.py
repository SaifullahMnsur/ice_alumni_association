import os
from django.db import models
from django.core.validators import RegexValidator
from tinymce.models import HTMLField
from django.core.exceptions import ValidationError
from django.utils.text import slugify

def event_media_upload_to(instance, filename):
    """Generate file path for the event media file using event_id."""
    
    file_extension = os.path.splitext(filename)[1]
    
    return os.path.join('event_media', instance.event_id + file_extension)

class Event(models.Model):
    event_id = models.SlugField(
        max_length=50,
        unique=True,
        primary_key=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9-]+$',
                message="Event ID can only contain letters, numbers, and hyphens.",
            )
        ],
        verbose_name="Event ID"
    )
    title = models.CharField(max_length=200, verbose_name="Event Title")
    description = HTMLField(help_text="Rich HTML content for the event description.")
    
    start_time = models.DateTimeField(help_text="The start time of the event.")
    end_time = models.DateTimeField(help_text="The end time of the event.")
    location = models.CharField(max_length=255, blank=True, help_text="Location where the event will take place.")
    status = models.CharField(
        max_length=20,
        choices=[
            ('upcoming', 'Upcoming'),
            ('ongoing', 'Ongoing'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='upcoming',
        help_text="The current status of the event."
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="The time when the event was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="The last time the event was updated.")

    # Media file field
    media_file = models.FileField(
        upload_to=event_media_upload_to, null=True, blank=True, 
        help_text="Upload an image, gif, or video for the event."
    )
    
    amount_per_person = models.PositiveIntegerField(default=0, help_text="The amount per person for the event.")
    amount_per_adult_guest = models.PositiveIntegerField(default=0, help_text="The amount per person for the event.")
    amount_per_child_guest = models.PositiveIntegerField(default=0, help_text="The amount per person for the event.")

    def rename_media_files(self, old_event_id):
        """Rename the media file to the new event ID if applicable."""
        if self.media_file:
            old_media_path = self.media_file.path
            # Check if the old event ID is part of the filename
            if old_event_id in old_media_path:
                new_file_name = old_media_path.replace(old_event_id, self.event_id)
                new_media_path = os.path.join(os.path.dirname(old_media_path), os.path.basename(new_file_name))
                
                # Rename the file on the filesystem
                os.rename(old_media_path, new_media_path)
                
                # Update the media file field with the new path
                self.media_file.name = os.path.relpath(new_media_path, start=os.path.dirname(self.media_file.storage.location))

    # def save(self, *args, **kwargs):
    #     """Override save to handle renaming the event and its media file."""
    #     if not self.event_id:
    #         self.event_id = slugify(self.title)  # Ensure event_id is created if not set
        
    #     # If the event_id is changed, rename the media file associated with the event
    #     if self.pk:  # Check if this is an update (not a new instance)
    #         old_event = Event.objects.get(pk=self.pk)
    #         old_event_id = old_event.event_id
    #         if old_event_id != self.event_id:
    #             # Rename the media files
    #             self.rename_media_files(old_event_id)
        
    #     # Save the event object
    #     super().save(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        """Override save to handle renaming the event and its media file."""
        # Ensure event_id is created if not set
        if not self.event_id:
            self.event_id = slugify(self.title)  # Automatically generate event_id based on title
        
        # Check if this is an update (not a new instance)
        if self.pk:
            try:
                old_event = Event.objects.get(pk=self.pk)
                old_event_id = old_event.event_id
                if old_event_id != self.event_id:
                    # If event_id changed, rename associated media files
                    self.rename_media_files(old_event_id)
            except Event.DoesNotExist:
                pass  # In case the event does not exist, skip renaming (unlikely for update)
        
        # Save the event object
        super().save(*args, **kwargs)
        
    def clean(self):
        # Validate file type (image, gif, video)
        if self.media_file:
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mov', '.avi', '.webm']
            file_extension = os.path.splitext(self.media_file.name)[1].lower()
            if file_extension not in valid_extensions:
                raise ValidationError(f"Invalid file format. Allowed formats: {', '.join(valid_extensions)}")

    def __str__(self):
        return self.title
