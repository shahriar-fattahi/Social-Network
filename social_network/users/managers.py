from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password, is_active=True, is_admin=False):
        if not email:
            raise ValueError("Email must be entered")
        if not password:
            raise ValueError("Password must be entered")

        user = self.model(
            email=self.normalize_email(email),
            is_active=is_active,
            is_admin=is_admin,
        )
        user.set_password(password)
        user.full_clean()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=email,
            password=password,
            is_active=True,
            is_admin=True,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user
