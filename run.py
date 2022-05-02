import os


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linker.settings')
    os.system('python manage.py runserver')


if __name__ == '__main__':
    main()
