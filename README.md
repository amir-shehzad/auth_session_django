# Rate-Limiting Login Attempts in Django with Custom Session Authentication

This is a Django project built with Python 3.9.

## Installation

1. Clone the repository:

```shell
git clone https://github.com/amir-shehzad/auth_session_django.git
```

2. Create a virtual environment and activate it:

```shell
python3 -m venv env
source env/bin/activate  # for Linux/Mac
env\Scripts\activate  # for Windows
```

3. Install the required packages:

```shell
pip install -r requirements.txt
```

## Superuser Account

A superuser account has already been created for this Django project. You can use the following credentials to access the admin panel:

```json
{
    "username": "aamir",
    "password": "shehzad"
}
```

To log in as the superuser, run the Django development server:

```shell
python manage.py runserver
```

Then, visit `http://localhost:8000/admin` in your web browser and log in with the provided superuser credentials.

## URLs

- Login URL (POST): `http://localhost:8000/login`
    - Expects username and password in the request body.

- Authenticated URL (GET): `http://localhost:8000/authenticated`
    - Requires session_id for authentication. Accessible only to logged-in users.

- Reset Sessions URL (DELETE): `http://localhost:8000/reset_sessions`
    - Requires session_id for authentication. Deletes all user sessions and logs users out.
  
## Contributing

Contributions are welcome! If you have any suggestions, improvements, or bug fixes, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).