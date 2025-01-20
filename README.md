# dcs_enrollment_system

1. Create a Virtual Environment
   `python -m venv .venv`
2. Activate Virtual Environment
   `.venv/scripts/activate`
3. Install django
    `pip install django`
4. Install mysqlclient
   `pip install mysqlclient`
5. Install xhtml2pdf
   `pip install xhtml2pdf`
6. In mysql, create a database named dcs_enrolled_students
    `dcs_enrolled_students`
7. Check settings.py under enrollment_system directory and see if:
   * database details are correct
   * ![image](https://github.com/user-attachments/assets/2a2f26f9-46f0-4206-b6bc-430bb4cd6b74)
8. Run makemigrations
    `python manage.py makemigrations`
9. Run migrate
    `python manage.py migrate`
