
from decimal import Decimal

from django.db import transaction

from .models import ExpenseShare, GroupMembership


@transaction.atomic
def split_expense_equally(expense):
    member_ids = list(
        GroupMembership.objects.filter(
            group=expense.group
        )
        .order_by("user_id")
        .values_list("user_id", flat=True)
    )

    if not member_ids:
        raise ValueError(
            "Cannot split an expense without group members."
        )

    if expense.paid_by_id not in member_ids:
        raise ValueError(
            "The payer must be a member of the expense group."
        )

    total_cents = int(
        expense.amount * Decimal("100")
    )

    member_count = len(member_ids)

    base_cents, remainder = divmod(
        total_cents, member_count
    )

    # Replace previous shares when an expense is edited.
    ExpenseShare.objects.filter(
        expense=expense
    ).delete()

    shares = []

    for index, user_id in enumerate(member_ids):
        cents = base_cents

        if index < remainder:
            cents += 1

        shares.append(
            ExpenseShare(
                expense=expense,
                user_id=user_id,
                amount_owed=(
                    Decimal(cents) / Decimal("100")
                ),
            )
        )

    ExpenseShare.objects.bulk_create(shares)

    return shares
