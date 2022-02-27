from django.db import models


class Club(models.Model):
    def __str__(self):
        club_name = self.full_name or self.name
        return f"id: {self.id}, name: {club_name}"

    @staticmethod
    def get_all_clubs():
        return Club.objects.all()

    class Meta:
        verbose_name = "club"
        verbose_name_plural = "clubs"

    name = models.CharField(
        max_length=40)
    full_name = models.CharField(
        max_length=60,
        null=True,
        blank=True)
    description = models.CharField(
        max_length=200,
        null=True,
        blank=True)
    country = models.CharField(
        max_length=30,
        null=True,
        blank=True)


class Kudos(models.Model):
    class Meta:
        verbose_name = "kudos"
        verbose_name_plural = "kudos"

    @staticmethod
    def get_all_kudos():
        return Kudos.objects.order_by('-id')

    @staticmethod
    def get_last_hundred_kudos():
        return Kudos.objects.order_by('-id')[:100]

    club = models.ForeignKey(
        Club,
        null=True,
        on_delete=models.SET_NULL)
    date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        club = Club.objects.get(id=self.club_id)
        club_name = club.full_name or club.name

        return f"id: {self.id}, club_id: {self.club_id}, club_name: " \
               f"{club_name}, date: {self.date}"

