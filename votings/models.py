from django.db import models
from django.conf import settings
from django.utils import timezone


class VotingStates():
    PLANNED = 1
    SCHEDULED = 2
    ACTIVE = 3
    FINISHED = 4

    
class Assembly(models.Model):
    name_text = models.CharField(max_length=128, null=False, blank=False)
    description_text = models.TextField(max_length=256, null=False, blank=True)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, null=True, blank=True)
    is_main = models.BooleanField(default=False, null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_text


class Membership(models.Model):
    assembly = models.ForeignKey(Assembly, on_delete=models.RESTRICT, null=False, blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, null=False, blank=False)
    start_date = models.DateTimeField(null=False, blank=False)
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.start_date) + ' ----- ' + str(self.end_date)


class Voting(models.Model):
    title_text = models.CharField(max_length=128, null=False, blank=False)
    question_text = models.CharField(max_length=256, null=False, blank=False)
    explanation_text = models.TextField(max_length=512, blank=True)
    assembly = models.ForeignKey(Assembly, on_delete=models.RESTRICT, null=False, blank=False)
    are_votes_anonymous = models.BooleanField(null=False, blank=False, default=True)
    is_public = models.BooleanField(default=False)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    electorate_quantity = models.PositiveIntegerField(null=True, blank=True)
    votes_quantity = models.PositiveIntegerField(null=True, blank=True)
    state = models.PositiveSmallIntegerField(null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title_text

    def update_state(self):
        now = timezone.now()
        if self.end_date == None or self.start_date == None:
            self.state = VotingStates.PLANNED
        elif now < self.start_date:
            self.state = VotingStates.SCHEDULED
        elif now < self.end_date:
            self.state = VotingStates.ACTIVE
        elif now >= self.end_date:
            self.state = VotingStates.FINISHED


class Option(models.Model):
    index_number = models.IntegerField(null=True, blank=True)
    title_text = models.CharField(max_length=128, null=False, blank=False)
    explanation_text = models.TextField(max_length=512, blank=True)
    votes_quantity = models.PositiveIntegerField(null=True, blank=True)
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return '(' + str(self.index_number) +  ') ' + self.title_text


class Vote(models.Model):
    option = models.ForeignKey(Option, on_delete=models.RESTRICT, null=False, blank=False)

    def __str__(self):
        return str(self.id) + ': ' + str(self.option.index_number)


class Participation(models.Model):
    voting = models.ForeignKey(Voting, on_delete=models.RESTRICT, null=False, blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, null=False, blank=False)
    vote = models.OneToOneField(Vote, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.voting.id) + ': ' + str(self.user.id)


class ParticipationTemporaryRecord(models.Model):
    voting = models.ForeignKey(Voting, on_delete=models.RESTRICT, null=False, blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, null=False, blank=False)

    def __str__(self):
        return str(self.voting.id) + ': ' + str(self.user.id)


class Tag(models.Model):
    name_text = models.CharField(max_length=128, null=False, blank=False)
    voting = models.ManyToManyField(Voting, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_text