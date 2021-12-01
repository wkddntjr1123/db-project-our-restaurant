from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.deletion import CASCADE, PROTECT


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, user_id, name, nickname, password=None):
        user = self.model(user_id=user_id, name=name, nickname=nickname)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, name, nickname, password):
        user = self.create_user(user_id=user_id, name=name, nickname=nickname, password=password)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


# 유저 엔티티
class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=10)
    nickname = models.CharField(max_length=20, null=False, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    joined_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user"

    objects = UserManager()

    USERNAME_FIELD = "user_id"
    REQUIRED_FIELDS = ["name", "nickname"]


# 그룹 엔티티
class Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    manager = models.ForeignKey(User, on_delete=PROTECT, related_name="manager")

    class Meta:
        db_table = "group"


class GroupAndMember(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=CASCADE)
    group = models.ForeignKey(Group, on_delete=CASCADE)
    accept = models.BooleanField(default=False)

    class Meta:
        db_table = "user_and_group"
