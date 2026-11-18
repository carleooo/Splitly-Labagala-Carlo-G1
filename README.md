
# Splitly — Group Expense Sharing System

Splitly is a Django-based expense-sharing application designed to help friends, students, and roommates organize shared expenses.

## Project Development 2 — Core Feature

The implemented core feature is **Group Expense Tracking and Equal Splitting**.

### Features

- Account registration, login, and logout
- Admin and Member dashboards
- User profile viewing and editing
- Create, view, edit, and delete expense groups
- Add existing Splitly users to expense groups
- Record shared expenses and select who paid
- Split expenses equally among group members
- View each member's calculated share
- Edit and delete expenses created by the logged-in user
- Validate expense amounts and group information
- Restrict access based on group membership and ownership
- Store records in Supabase PostgreSQL

## Technology Stack

- Python
- Django
- PostgreSQL / Supabase
- HTML, CSS, Bootstrap
- Git and GitHub

## Local Setup

1. Clone the repository:

   git clone https://github.com/carleooo/Splitly-Labagala-Carlo-G1.git

2. Enter the project directory:

   cd Splitly-Labagala-Carlo-G1

3. Create and activate a virtual environment:

   py -m venv venv
   .\venv\Scripts\Activate.ps1

4. Install dependencies:

   python -m pip install -r requirements.txt

5. Create a `.env` file in the project root with:

   DJANGO_SECRET_KEY=your_secret_key
   DB_NAME=postgres
   DB_USER=your_supabase_pooler_username
   DB_PASSWORD=your_database_password
   DB_HOST=your_supabase_pooler_host
   DB_PORT=5432

6. Apply database migrations:

   python manage.py migrate

7. Start the application:

   python manage.py runserver

8. Open:

   http://127.0.0.1:8000/login/

## Using the Core Feature

1. Register or log in.
2. Open the Admin or Member Dashboard.
3. Select **Manage Groups**.
4. Create an expense group.
5. Add existing Splitly users as members.
6. Open the group's **View Expenses** page.
7. Select **Add Expense**.
8. Enter the expense title, amount, and payer.
9. Save the expense to calculate the equal shares.
10. View, edit, or delete expenses as permitted.

## Access Control

- Only authenticated users can access group and expense pages.
- Group members can view their groups and recorded expenses.
- Only group creators can edit or delete groups and add members.
- Only expense creators can edit or delete their expenses.
- Administrators use the same group ownership restrictions for this feature.

## Current Limitations

- Expenses are divided equally among group members.
- Custom unequal splits are not implemented.
- Consolidated net balances and settlements are not yet implemented.
- Adding a group member does not recalculate previously saved expenses automatically.

## Branching Strategy

- `main` — Stable project
- `develop` — Integration branch
- `feature/expense-groups` — Expense Groups implementation
- `feature/expense-splitting` — Expense Tracking and Equal Splitting

Development follows feature branch → Pull Request into develop → Pull Request into main.
