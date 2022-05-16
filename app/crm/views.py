import json
import uuid

from aiohttp import web
from aiohttp.web_response import json_response

from app.crm.models import User


class AddUserView(web.View):
    async def post(self):
        data = await self.request.json()
        user = User(email=data['email'], _id=uuid.uuid4())
        await self.request.app.crm_accessor.add_user(user)
        return json_response(data={'status': 'OK'})

        
class ListUserView(web.View):
    async def get(self):
        users = await self.request.app.crm_accessor.list_users()
        raw_users = [{'email': user.email, '_id': str(user._id)} for user in users]
        return json_response(data={'status': 'OK', 'users': raw_users})
    

class GetUserView(web.View):
    async def get(self):
        user_id = self.request.query['id']
        user = await self.request.app.crm_accessor.get_user(uuid.UUID(user_id))
        return json_response(data={'status': 'OK', 'user': {'email': user.email, 'id': str(user._id)}})

        