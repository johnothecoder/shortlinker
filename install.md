# Installation

## Local Development

Clone the repository and move into the project directory:

```
git clone https://github.com/johnothecoder/shortlinker.git
cd shrtlnkr
```

Create and activate a virtual environment:

```
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```
.venv\Scripts\activate
```

Install the required packages:

```
python -m pip install -r requirements.txt
```
Apply the database migrations:

```
python manage.py migrate
```

Create an administrator account:

```
python manage.py createsuperuser
```

Start the development server:

```
python manage.py runserver
```

The application will be available at: http://127.0.0.1:8000/

The Django administration panel is available at: http://127.0.0.1:8000/admin/

# Production Deployment

This project is a standard Django application and can be deployed using any suitable WSGI-compatible hosting setup.

Create and activate a virtual environment, then install the pinned dependencies:

```
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Configure the required production settings, including:

```
DEBUG = False
ALLOWED_HOSTS = ["your-domain.example"]
```

Do not commit production secrets directly to the repository. Provide values such as SECRET_KEY, database credentials and allowed hosts through environment variables or another secure configuration method.

Apply the database migrations:

```
python manage.py migrate
```

Collect the static files:

```
python manage.py collectstatic
```

Create an administrator account if required:

```
python manage.py createsuperuser
```

The application can then be served using Gunicorn:

```
gunicorn config.wsgi:application
```

In a typical production setup, Gunicorn should run behind a reverse proxy such as Nginx or Apache. The reverse proxy should:

* Forward application requests to Gunicorn.
* Serve the collected static files from STATIC_ROOT.
* Provide HTTPS using a valid TLS certificate.
* Pass the original request host, protocol and client information to Django.

Gunicorn should normally be managed by a process supervisor such as systemd, rather than started manually in a terminal.

Before exposing the application publicly, run Django’s deployment checks:

```
python manage.py check --deploy
```