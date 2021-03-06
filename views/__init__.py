"""
Module contains all views blueprints.

Blueprints:
    api
    api_departments
    api_employees
    api_login
    api_users
"""
import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))


from .views_departments import api_departments
from .views_employees import api_employees
from .views_login import api_login
from .views_users import api_users






























