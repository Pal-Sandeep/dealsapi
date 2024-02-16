from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Project(models.Model):
    """Model for storing Project related data"""

    name = models.CharField(max_length=255)
    fmv = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Deal(models.Model):
    """Model for storing Deal related data"""

    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class DealProject(models.Model):
    """Model for storing projects in deal"""

    deal = models.ForeignKey(
        Deal, on_delete=models.CASCADE, related_name='projects')
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='deals')
    tax_credit_transfer_rate = models.DecimalField(
        max_digits=3, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(1.0)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.deal.name}-{self.project.name}"

    def get_tax_credit_transfer_rate(self, obj):
        return str(obj.tax_credit_transfer_rate)

    def get_tax_credit_amount(self):
        return self.project.fmv * Decimal(0.3) * self.tax_credit_transfer_rate

    class Meta:
        unique_together = ('deal', 'project')
