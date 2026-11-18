
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ExpenseGroupForm, AddGroupMemberForm
from .models import ExpenseGroup, GroupMembership


User = get_user_model()


@login_required
def group_list(request):
    groups = (
        ExpenseGroup.objects.filter(
            Q(created_by=request.user) |
            Q(memberships__user=request.user)
        )
        .distinct()
        .order_by("-created_at")
    )

    return render(request, "expenses/group_list.html", {
        "groups": groups,
    })


@login_required
def group_create(request):
    if request.method == "POST":
        form = ExpenseGroupForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                group = form.save(commit=False)
                group.created_by = request.user
                group.save()

                GroupMembership.objects.create(
                    group=group,
                    user=request.user,
                )

            messages.success(
                request, "Expense group created successfully!"
            )
            return redirect("expenses:group_detail", pk=group.pk)
    else:
        form = ExpenseGroupForm()

    return render(request, "expenses/group_form.html", {
        "form": form,
        "page_title": "Create Expense Group",
        "button_text": "Create Group",
    })


@login_required
def group_detail(request, pk):
    group = get_object_or_404(
        ExpenseGroup.objects.filter(
            Q(created_by=request.user) |
            Q(memberships__user=request.user)
        ).distinct(),
        pk=pk,
    )

    memberships = group.memberships.select_related("user")
    is_owner = group.created_by_id == request.user.pk

    return render(request, "expenses/group_detail.html", {
        "group": group,
        "memberships": memberships,
        "is_owner": is_owner,
        "member_form": AddGroupMemberForm() if is_owner else None,
    })


@login_required
def group_edit(request, pk):
    group = get_object_or_404(
        ExpenseGroup,
        pk=pk,
        created_by=request.user,
    )

    if request.method == "POST":
        form = ExpenseGroupForm(request.POST, instance=group)

        if form.is_valid():
            form.save()
            messages.success(
                request, "Expense group updated successfully!"
            )
            return redirect("expenses:group_detail", pk=group.pk)
    else:
        form = ExpenseGroupForm(instance=group)

    return render(request, "expenses/group_form.html", {
        "form": form,
        "page_title": "Edit Expense Group",
        "button_text": "Save Changes",
    })


@login_required
@require_POST
def group_delete(request, pk):
    group = get_object_or_404(
        ExpenseGroup,
        pk=pk,
        created_by=request.user,
    )

    group.delete()

    messages.success(
        request, "Expense group deleted successfully!"
    )
    return redirect("expenses:group_list")


@login_required
@require_POST
def group_add_member(request, pk):
    group = get_object_or_404(
        ExpenseGroup,
        pk=pk,
        created_by=request.user,
    )

    form = AddGroupMemberForm(request.POST)

    if form.is_valid():
        username = form.cleaned_data["username"]

        user = User.objects.filter(
            username__iexact=username
        ).first()

        if user is None:
            messages.error(
                request, "No user found with that username."
            )
        else:
            membership, created = (
                GroupMembership.objects.get_or_create(
                    group=group,
                    user=user,
                )
            )

            if created:
                messages.success(
                    request,
                    f"{user.username} added to the group!"
                )
            else:
                messages.warning(
                    request,
                    "This user is already a group member."
                )
    else:
        messages.error(
            request, "Please enter a valid username."
        )

    return redirect("expenses:group_detail", pk=group.pk)
