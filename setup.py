from setuptools import setup, find_packages

setup(
    name='currency_converter',
    version='1.0',
    packages=find_packages(),
    scripts=['scripts/init_db.sh', 'scripts/run.sh']
    # entry_points={
    #     'console_scripts': [
    #         'init-db=currency_converter.cli:init_db_command'
    #     ]
    # }
)