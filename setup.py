from distutils.core import setup
import os

setup(
    name = 'django_cropper',
    packages = ['cropper'],
    package_dir = {
        'cropper': 'cropper'
    },
    package_data = {
        'cropper': ['templates/cropper/*.html']
    },
    version = '0.1.4a',
    description = 'Image cropping for the Django admin',
    author = 'Simon Willison',
    author_email = 'simon@simonwillison.net',
    url = 'http://github.com/simonw/django_cropper',
    keywords = ['pil', 'django', 'cropping', 'image'],
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
    ],
    long_description = open(
        os.path.join(os.path.dirname(__file__), 'README.txt')
    ).read().strip(),
)
