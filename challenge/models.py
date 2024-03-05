from django.db import models

# Create your models here.

DIFFICULTY_CHOICES = ((1, "آسان"), (2, "متوسط"), (3, "سخت"))
CHALLENGE_TYPE = ((1, "معمایی"), (2, "چالشی"), (3, "ترکیبی"))
USER_MISSION_ACCEPTANCE = ((1, "تایید نشده"), (2, "در انتظار تایید"), (3, "تایید شده"))
MISSION_TYPE = ((1, "معمایی"), (2, "چالشی"))


class Challenge(models.Model):
    name = models.CharField(verbose_name="challenge name", max_length=50)
    description = models.TextField(verbose_name="challenge description")
    enter_price = models.IntegerField(verbose_name="challenge enter price", default=0)
    reward_price = models.IntegerField(verbose_name="challenge reward price", default=0)
    attended_number = models.IntegerField(verbose_name="challenge attended number", default=0)
    mission_count = models.IntegerField(verbose_name="challenge mission count", default=0)
    difficulty = models.IntegerField(verbose_name="challenge difficulty", choices=DIFFICULTY_CHOICES, default=0)
    start_time = models.DateTimeField(verbose_name="challenge start time")
    end_time = models.DateTimeField(verbose_name="challenge end time")
    status = models.BooleanField(verbose_name="challenge status", default=True)
    challenge_type = models.IntegerField(verbose_name="mission type", choices=CHALLENGE_TYPE, default=1)

    def __str__(self):
        """String representation of model"""

        return self.name

    class Meta:
        """Passing model metadata"""

        verbose_name = ("مسابقه")
        verbose_name_plural = ("مسابقات")


class Mission(models.Model):
    name = models.CharField(verbose_name="mission name", max_length=50)
    description = models.TextField(verbose_name="mission description")
    mission_type = models.IntegerField(verbose_name="mission type", choices=MISSION_TYPE, default=1)
    correct_answers = models.TextField(verbose_name="mission correct answers", null=True, blank=True)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, blank=True,
                                     verbose_name="mission challenge id", default=0)
    # challenge_id = models.IntegerField(verbose_name="mission_challenge_id", default=0)
    mission_order = models.IntegerField(verbose_name="mission order", default=0)

    def __str__(self):
        """String representation of model"""

        return self.name

    class Meta:
        """Passing model metadata"""

        verbose_name = ("مرحله")
        verbose_name_plural = ("مراحل")


class UserChallenge(models.Model):
    user_id = models.IntegerField(verbose_name="userChallenge user id", default=0)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, blank=True, verbose_name="userchallenge_challenge")
    register_time = models.DateTimeField(verbose_name="user challenge register_time", auto_now_add=True)
    current_mission = models.ForeignKey(Mission, on_delete=models.CASCADE, blank=True, verbose_name="userchallenge_current_mission", default=1)

    class Meta:
        """Passing model metadata"""

        verbose_name = ("مسابقه کاریر")
        verbose_name_plural = ("مسابقات کاربر")

class UserMission(models.Model):
    user_id = models.IntegerField(verbose_name="user mission user id", default=0)
    mission_id = models.ForeignKey(Mission, on_delete=models.CASCADE, blank=True, verbose_name="user_mission_mission_id", default=0)
    status = models.BooleanField(verbose_name="user mission status", default=True)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, blank=True, verbose_name="user_mission_challenge", default=0)
    video_id = models.IntegerField(verbose_name="user mission video_id", null=True, blank=True, default=0)
    image_id = models.IntegerField(verbose_name="user mission image_id", null=True, blank=True, default=0)
    answer = models.CharField(verbose_name="user mission answer",max_length=50, null=True, blank=True, default=0)
    time = models.DateTimeField(verbose_name="user mission time", auto_now_add=True)
    like_video = models.IntegerField(verbose_name="user mission like video", default=0)
    acceptance = models.IntegerField(verbose_name="user mission acceptance", choices=USER_MISSION_ACCEPTANCE, default=1)


    class Meta:
        """Passing model metadata"""

        verbose_name = ("مرحله ی کاریر")
        verbose_name_plural = ("مراحل کاربر")


