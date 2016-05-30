from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from ledger.accounts.models import RevisionedMixin, EmailUser, Document, Profile
from ledger.licence.models import LicenceType, Licence


@python_2_unicode_compatible
class Condition(RevisionedMixin):
    text = models.TextField()
    code = models.CharField(max_length=10, unique=True)
    one_off = models.BooleanField(default=False)
    obsolete = models.BooleanField(default=False)

    def __str__(self):
        return self.code


class WildlifeLicenceType(LicenceType):
    identification_required = models.BooleanField(default=False)
    default_conditions = models.ManyToManyField(Condition, through='DefaultCondition', blank=True)


class WildlifeLicence(Licence):
    profile = models.ForeignKey(Profile)
    sequence_number = models.IntegerField(default=1)
    purpose = models.TextField(blank=True)
    cover_letter_message = models.TextField(blank=True)
    licence_document = models.ForeignKey(Document, blank=True, null=True, related_name='licence_document')
    cover_letter_document = models.ForeignKey(Document, blank=True, null=True, related_name='cover_letter_document')
    previous_licence = models.ForeignKey('self', blank=True, null=True)


class DefaultCondition(models.Model):
    condition = models.ForeignKey(Condition)
    wildlife_licence_type = models.ForeignKey(WildlifeLicenceType)
    order = models.IntegerField()

    class Meta:
        unique_together = ('condition', 'wildlife_licence_type', 'order')


class AbstractLogEntry(models.Model):
    user = models.ForeignKey(EmailUser, null=False, blank=False)
    text = models.TextField(blank=True)
    document = models.ForeignKey(Document, null=True, blank=False)
    created = models.DateField(auto_now_add=True, null=False, blank=False)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class AssessorGroup(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    members = models.ManyToManyField(EmailUser, blank=True)
    purpose = models.BooleanField(default=False)

    def __str__(self):
        return self.name
