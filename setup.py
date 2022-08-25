from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name='aiogram_timepicker',
  packages=['aiogram_timepicker'],
  version='0.0.1',
  license='MIT',
  description='Simple Inline Time Selection tool for Aiogram Telegram bots',
  long_description=long_description,
  author='Marat Ashrafzianov',
  author_email='marat.ashraf@yandex.ru',
  url='https://github.com/maratx86/aiogram-timepicker',
  download_url='https://github.com/maratx86/aiogram-timepicker/archive/refs/tags/0.0.1.tar.gz',
  keywords=['Aiogram', 'Telegram', 'Bots', 'Time', 'Timepicker'],
  install_requires=[
          'aiogram',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
