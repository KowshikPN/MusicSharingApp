import graphene
import tracks.schema
import users.schema
import graphql_jwt

#root query
class Query(users.schema.Query, tracks.schema.Query, graphene.ObjectType):
    pass

class Mutation(users.schema.Mutation, tracks.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


#creates a schema to query the tracks app.
schema = graphene.Schema(query=Query,mutation=Mutation)