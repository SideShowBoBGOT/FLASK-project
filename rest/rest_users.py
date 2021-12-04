from flask_restful import Resource, abort, reqparse
import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from .common_funcs import check_empty_strings
from models.users import User
from service import add_user, del_user, change_user
from f_logger import logger

get_args = reqparse.RequestParser()
get_args.add_argument("login", type=str, help="User`s login", required=True)
get_args.add_argument("password", type=str, help="User`s password", required=True)

add_args = reqparse.RequestParser()
add_args.add_argument("login", type=str, help="User`s login", required=True)
add_args.add_argument("password", type=str, help="User`s password", required=True)
add_args.add_argument("new_login", type=str, help="Login of new user", required=True)
add_args.add_argument("new_password", type=str, help="Password of new user", required=True)

edit_args = reqparse.RequestParser()
edit_args.add_argument("login", type=str, help="User`s login", required=True)
edit_args.add_argument("password", type=str, help="User`s password", required=True)
edit_args.add_argument("new_login", type=str, help="New user`s login", required=True)
edit_args.add_argument("new_password", type=str, help="New user`s password", required=True)
edit_args.add_argument("id", type=int, help="Id of the user to edit", required=True)

del_args = reqparse.RequestParser()
del_args.add_argument("login", type=str, help="User`s login", required=True)
del_args.add_argument("password", type=str, help="User`s password", required=True)
del_args.add_argument("id", type=int, help="Id of the user to delete", required=True)


class UserAPIget(Resource):
    def post(self):
        args = get_args.parse_args()
        login = args['login']
        password = args['password']
        user = User.query.filter_by(login=login).first()
        if user and user.password == password:
            # admin`s id is 1
            if user.id == 1 and user.password == password:
                users = dict()
                for usr in User.query.all():
                    users[usr.id] = {'id': usr.id, 'login': usr.login,
                                     'password': usr.password}
                return users
            return {'id': user.id, 'login': user.login,
                    'password': user.password}
        abort(401, error='CREDENTIALS_INCORRECT')


class UserAPIadd(Resource):
    def post(self):
        args = add_args.parse_args()
        login = args['login']
        password = args['password']
        user = User.query.filter_by(login=login).first()
        new_login = args['new_login']
        new_password = args['new_password']
        if user and user.id == 1 and user.password == password:
            if check_empty_strings(new_login, new_password):
                if not User.query.filter_by(login=new_login).first():
                    add_user(new_login, new_password)
                    logger.info(f'Added user: new_login: "{new_login}"\tnew_password: "{new_password}"')
                    return {'message': 'ADD_SUCCESS'}
            logger.info(f'Failed adding user: new_login: "{new_login}"\tnew_password: "{new_password}"')
            abort(401, error='VALUES_INCORRECT')
        logger.info(f'Failed adding user: incorrect login: "{login}" or password: "{password}"')
        abort(401, error='CREDENTIALS_INCORRECT')


class UserAPIedit(Resource):
    def post(self):
        args = edit_args.parse_args()
        login = args['login']
        password = args['password']
        user = User.query.filter_by(login=login).first()
        new_login = args['new_login']
        new_password = args['new_password']
        id = args['id']
        if user and user.id == 1 and user.password == password:
            if check_empty_strings(new_login, new_password) and User.query.get(id) \
                    and (not User.query.filter_by(login=new_login).first() or User.query.get(id).login == new_login):
                change_user(id, new_login, new_password)
                logger.info(f'Edited user: id: "{id}" new_login: "{new_login}"\tnew_password: "{new_password}"')
                return {'message': 'EDIT_SUCCESS'}
            logger.info(f'Edited user: id: "{id}" new_login: "{new_login}"\tnew_password: "{new_password}"')
            abort(401, error='VALUES_INCORRECT')
        logger.info(f'Failed editing user: "{login}"\tpassword: "{password}"')
        abort(401, error='CREDENTIALS_INCORRECT')


class UserAPIdel(Resource):
    def post(self):
        args = del_args.parse_args()
        login = args['login']
        password = args['password']
        user = User.query.filter_by(login=login).first()
        # admin`s id is 1
        if user and user.id == 1 and user.password == password:
            id = args['id']
            if User.query.get(id):
                if id != 1:
                    del_user(id)
                    logger.info(f'Deleted user: id: "{id}"')
                    return {'message': 'DEL_SUCCESS'}
            logger.info(f'Failed deleting user: id: "{id}"')
            abort(401, error='VALUES_INCORRECT')
        logger.info(f'Failed deleting user: "{login}"\tpassword: "{password}"')
        abort(401, error='CREDENTIALS_INCORRECT')