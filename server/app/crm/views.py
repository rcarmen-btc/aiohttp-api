import json
import re
import uuid

from aiohttp import request, web
from aiohttp_apispec import docs, request_schema, response_schema, setup_aiohttp_apispec, querystring_schema
from aiohttp.web_exceptions import HTTPNotFound, HTTPUnauthorized, HTTPForbidden

from app.crm.models import User
from app.crm.schemes import GetUserResponseSchema, ListUsersResponseSchema, UserAddSchema, UserGetRequestSchema, UserGetSchema, UserSchema
from app.web.schemes import OkResponseSchema
from app.web.utils import chech_basic_auth, json_response


class AddUserView(web.View):
    @docs(tags=['crm'], summary='Add new user', description='Add new user')
    @request_schema(UserAddSchema)
    @response_schema(OkResponseSchema, 200)
    async def post(self):
        data = self.request['data']
        user = User(email=data['email'], _id=uuid.uuid4())
        await self.request.app.crm_accessor.add_user(user)
        return json_response()

        
class ListUserView(web.View):
    @docs(tags=['crm'], summary='List users', description='List users for db')
    @response_schema(ListUsersResponseSchema, 200)
    async def get(self):
        if not self.request.headers.get('Authorization'):
            raise HTTPUnauthorized
        if not chech_basic_auth(self.request.headers['Authorization'], username=self.request.app.config.username, password=self.request.app.config.password): 
            raise HTTPForbidden
        users = await self.request.app.crm_accessor.list_users()
        raw_users = [UserSchema().dump(user) for user in users]
        return json_response(data={'users': raw_users})
    

class GetUserView(web.View):
    @docs(tags=['crm'], summary='Get user', description='Get user from db')
    @querystring_schema(UserGetRequestSchema)
    @response_schema(GetUserResponseSchema, 200)
    async def get(self):
        if not self.request.headers.get('Authorization'):
            raise HTTPUnauthorized
        if not chech_basic_auth(self.request.headers['Authorization'], username=self.request.app.config.username, password=self.request.app.config.password): 
            raise HTTPForbidden
        user_id = self.request.query['id']
        user = await self.request.app.crm_accessor.get_user(uuid.UUID(user_id))
        if user:
            return json_response(data={'user': UserSchema().dump(user)})
        else:
            raise HTTPNotFound

        