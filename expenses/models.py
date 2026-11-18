
from django.conf import settings
from django.db import models


class ExpenseGroup(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_expense_groups"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class GroupMembership(models.Model):
    group = models.ForeignKey(
        ExpenseGroup,
        on_delete=models.CASCADE,
        related_name="memberships"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="expense_group_memberships"
    )

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["group", "user"],
                name="unique_group_membership"
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.group.name}"


from decimal import Decimal

from django.core.validators import MinValueValidator


class Expense(models.Model):
    group = models.ForeignKey(
        ExpenseGroup,
        on_delete=models.CASCADE,
        related_name="expenses"
    )

    title = models.CharField(max_length=150)

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.01"))
        ]
    )

    paid_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="paid_expenses"
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_expenses"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - ₱{self.amount}"


class ExpenseShare(models.Model):
    expense = models.ForeignKey(
        Expense,
        on_delete=models.CASCADE,
        related_name="shares"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="expense_shares"
    )

    amount_owed = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["expense", "user"],
                name="unique_expense_user_share"
            )
        ]

    def __str__(self):
        return f"{self.user.username} owes ₱{self.amount_owed}"

