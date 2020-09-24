import graphene
import tracks.schema
import users.schema

#root query
class Query(users.schema.Query, tracks.schema.Query, graphene.ObjectType):
    pass

class Mutation(users.schema.Mutation, tracks.schema.Mutation, graphene.ObjectType):
    pass

#creates a schema to query the tracks app.
schema = graphene.Schema(query=Query,mutation=Mutation)