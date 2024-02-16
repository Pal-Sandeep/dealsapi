# DealsAPI

This is a Django project for building a backend API to manage Deals and Projects.

## Project Setup
1. Clone the repository.
    ```git clone https://github.com/pal-sandeep/dealsapi.git```
2. Set up a virtual environment:
   ```python -m venv env```
3. Activate the virtual environment.
    ```source env/bin/activate```
4. Install the project dependencies:
    ```pip install -r requirements.txt```
5. Create the database migrations:
    ```python manage.py makemigrations```
6. Apply the database migrations:
    ```python manage.py migrate```
7. To run the project, use the following command:
    ```python manage.py runserver```