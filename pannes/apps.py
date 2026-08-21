from django.apps import AppConfig

class PannesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pannes'

    def ready(self):
        import os
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        username = os.environ.get('ADMIN_USERNAME', 'admin')
        email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
        password = os.environ.get('ADMIN_PASSWORD', 'Admin12345!')

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            print("Superuser créé avec succès !")
