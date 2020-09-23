'''
Author: Kowshik Prasad Navilur
Dependency: graphene module can be installed using $pipenv install graphene
To start the pipenv use $pipenv shell
This script can be executed from the terminal using $python schema.py
'''

import graphene
import json
from datetime import datetime
import uuid

class User(graphene.ObjectType):
    id = graphene.ID(default_value=str(uuid.uuid4()))
    username = graphene.String()
    created_at = graphene.DateTime(default_value=datetime.now())
    avatar_url = graphene.String()

    def resolve_avatar_url(self,info):
        return 'https://cloudinary.com/{}/{}'.format(self.username,self.id)

class Post(graphene.ObjectType):
    title = graphene.String()
    content = graphene.String()

class Query(graphene.ObjectType):
    users = graphene.List(User, limit=graphene.Int())
    hello = graphene.String()
    is_admin = graphene.Boolean()

    #resolve_ should be preappended to the name
    def resolve_hello(self,info):
        return "world"

    def resolve_is_admin(self,info):
        return True

    def resolve_users(self,info,limit=None):
        return [
            User(id="1",username="Fred",created_at=datetime.now()),
            User(id="2", username="John", created_at=datetime.now())
        ][:limit]

class CreateUser(graphene.Mutation):
    user = graphene.Field(User)
    class Arguments:
        username = graphene.String()


    #resolver method
    def mutate(self,info,username):
        user = User(username=username)
        return CreateUser(user=user)

class CreatePost(graphene.Mutation):
    post = graphene.Field(Post)
    class Arguments:
        title = graphene.String()
        content = graphene.String()

    #resolver method
    def mutate(self, info, title, content):
        if(info.context.get('is_anonymous')):
            raise Exception('Not Authenticated')
        post = Post(title=title, content=content)
        return CreatePost(post=post)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_post = CreatePost.Field()

schema = graphene.Schema(query=Query,mutation=Mutation)

query1 = schema.execute(
    '''
    {
    hello
    }
    '''
)
query2 = schema.execute(
    '''
    {
    isAdmin
    }
    '''
)
query3 = schema.execute(
    '''
    {
    users(limit:1){
    id
    username
    createdAt
    }
    }
    '''
)
query4 = schema.execute(
    '''    
    mutation($username: String){
        createUser(username: $username){
                    user{
                            id
                            username
                            createdAt
                        }
                    }
         }
    ''',
    variable_values={ 'username': "Dave"}
)

query5 = schema.execute(
    '''
    mutation{
        createPost(title:"Hello",content:"World"){
            post{
                title
                content        
            }
        }
    }
    ''',
    context={'is_anonymous': True} #Prevents unauthorized users to create a post
)

query6 = schema.execute(
    '''
    {
    users{
        id
        createdAt
        username
        avatarUrl
    }
    }
    '''
)

query1 = dict(query1.data.items())
query2 = dict(query2.data.items())
query3 = dict(query3.data.items())
query4 = dict(query4.data.items())
query5 = dict(query5.data.items())
query6 = dict(query6.data.items())

json_output1 = json.dumps(query1, indent=2)
json_output2 = json.dumps(query2, indent=2)
json_output3 = json.dumps(query3, indent=2)
json_output4 = json.dumps(query4, indent=2)
json_output5 = json.dumps(query5, indent=2)
json_output6 = json.dumps(query6,indent=2)

print(json_output1)

print(json_output2)

print(json_output3)

print(json_output4)

print(json_output5)

print(json_output6)