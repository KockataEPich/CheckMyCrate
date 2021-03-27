from setuptools import setup


setup(
    name='CheckMyCrate',
    version = '0.1',
    py_modules=['CheckMyCrate'],
    install_requires=[
        'Click',
        ],
    entry_points='''
        [console_scripts]
        CheckMyCrate=CheckMyCrate:program
        ''',
)
