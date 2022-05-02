import os

from django.core.management import execute_from_command_line


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linker.settings')
    execute_from_command_line(['manage.py', 'makemigrations', 'main'])
    execute_from_command_line(['manage.py', 'migrate'])
    execute_from_command_line(['manage.py', 'test'])
    os.system('python manage.py runserver')


if __name__ == '__main__':
    main()
