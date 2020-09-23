import graphene
import tracks.schema

#root query
class Query(tracks.schema.Query, graphene.ObjectType):
    pass

#creates a schema to query the tracks app.
schema = graphene.Schema(query=Query)