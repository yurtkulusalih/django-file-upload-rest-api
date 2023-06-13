from django.core.management import BaseCommand
from django.db import transaction
from django.contrib.auth.models import User

from config.dummyUser import DEFAULT_PASSWORD, USER_DATA


class Command(BaseCommand):
    help = """Adds/Syncs dummy user to database"""

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Syncing dummy users..."))

        for member_data in USER_DATA:
            self.stdout.write(f'Syncing user: {member_data["username"]}')

            user = self.exists(member_data["email"])
            if user:
                self.stdout.write(
                    f"""User {member_data["username"]} already exists! Updating \
                        privileges if changed."""
                )
                self.update_status_if_changed(user, member_data)
                continue

            user = self.create_user(member_data)
            self.stdout.write(
                f"""Created user {user.username} with specified data and default \
                    password."""
            )

        self.stdout.write(self.style.SUCCESS("Done!"))

    def exists(self, email):
        return User.objects.filter(email=email).first()

    def update_status_if_changed(self, user: User, member_data):
        updated = False

        if not user.is_superuser == member_data["is_superuser"]:
            user.is_superuser = member_data["is_superuser"]
            updated = True

        if not user.is_staff == member_data["is_staff"]:
            user.is_staff = member_data["is_staff"]
            updated = True

        if updated:
            user.save()

    def create_user(self, member_data):

        member_data["is_active"] = True
        user = User(**member_data)
        user.set_password(DEFAULT_PASSWORD)

        with transaction.atomic():
            user.save()

        return user
