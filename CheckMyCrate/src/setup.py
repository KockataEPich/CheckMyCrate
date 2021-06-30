from setuptools import setup


setup(
    name='CheckMyCrate',
    version = '0.2',
    py_modules=['CheckMyCrate'],
    install_requires=[
        'Click',
        ],
    entry_points='''
        [console_scripts]
        cmc=CheckMyCrate:program
        ''',
)
