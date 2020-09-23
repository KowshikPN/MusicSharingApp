import graphene
import json
from datetime import datetime
import uuid

class User(graphene.ObjectType):
    id = graphene.ID(default_value=str(uuid.uuid4()))
    username = graphene.String()
    created_at = graphene.DateTime(default_value=datetime.now())

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

    def mutate(self,info,username):
        user = User(username=username)
        return CreateUser(user=user)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()

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

query1 = dict(query1.data.items())
query2 = dict(query2.data.items())
query3 = dict(query3.data.items())
query4 = dict(query4.data.items())

json_output1 = json.dumps(query1, indent=2)
json_output2 = json.dumps(query2, indent=2)
json_output3 = json.dumps(query3, indent=2)
json_output4 = json.dumps(query4, indent=2)

print(json_output1)

print(json_output2)

print(json_output3)

print(json_output4)