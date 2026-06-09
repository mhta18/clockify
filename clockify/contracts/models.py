import os
from django.db import models
from users.models import User
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

class Contract(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="contract"
        , verbose_name=_("user")
    )
    role_title = models.CharField(max_length=255,
        verbose_name=_("role title"))
    start_date = models.DateField(null=False,
        verbose_name=_("start date"))
    end_date = models.DateField(null=False,
        verbose_name=_("end date"))
    is_terminated = models.BooleanField(default=False,
        verbose_name=_("is terminated"))
    created_at = models.DateTimeField(auto_now_add=True,
        verbose_name=_("created at"))

    class Meta:
        verbose_name =_("contract")
        verbose_name_plural= _("contracts")

    def __str__(self):
        return f"{self.role_title} - {self.user.email}"


class FreelancerContract(Contract):
    hourly_payment = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name=_("hourly payment")
    )
    daily_hours_required = models.PositiveIntegerField(
        verbose_name=_("daily hours required")
    )
    document_file = models.FileField(
        upload_to="freelancer_contracts/", 
        null=True, 
        blank=True,
        verbose_name=_("document file")
    )

    class Meta:
        verbose_name = _("freelancer contract")
        verbose_name_plural = _("freelancer contracts")


class EmployerContract(Contract):
    class EmploymentHours(models.IntegerChoices):
        FOUR_HOURS = 4, _("Part-time (4 Hours)")
        FIVE_HOURS = 5, _("Part-time (5 Hours)")
        SIX_HOURS = 6, _("Part-time (6 Hours)")
        SEVEN_HOURS = 7, _("Part-time (7 Hours)")
        EIGHT_HOURS = 8, _("Full-time (8 Hours)")

    monthly_payment = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name=_("monthly payment")
    )
    employment_type = models.IntegerField(
        choices=EmploymentHours.choices,
        default=EmploymentHours.EIGHT_HOURS,
        validators=[MinValueValidator(4), MaxValueValidator(8)],
        help_text=_("Designated daily contractual obligation commitment hours."),
        verbose_name=_("employment type")
    )

    class Meta:
        verbose_name = _("employer contract")
        verbose_name_plural = _("employer contracts")

@receiver(post_delete, sender=FreelancerContract)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.document_file:
        if os.path.isfile(instance.document_file.path):
            os.remove(instance.document_file.path)


@receiver(models.signals.pre_save, sender=FreelancerContract)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_contract = sender.objects.get(pk=instance.pk).document_file
    except sender.DoesNotExist:
        return False

    new_contract = instance.document_file

    if old_contract and old_contract != new_contract:
        if os.path.isfile(old_contract.path):
            os.remove(old_contract.path)
