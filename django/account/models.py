from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom user extends the standard Django user model, providing additional properties
    """

    @property
    def name(self):
        if self.first_name and self.last_name:
            return ' '.join((self.first_name, self.last_name))
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        else:
            # If no first or last name provided, return first half of email
            return self.username.split('@')[0]  # e.g. mike.allaway in mike.allaway@ox.ac.uk

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Username to be same as email
        self.username = self.email
        super().save(*args, **kwargs)
