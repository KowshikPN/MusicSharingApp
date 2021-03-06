import graphene
from graphene_django import DjangoObjectType
from .models import Track,Like
from users.schema import UserType
from graphql import GraphQLError
from django.db.models import  Q

class TrackType(DjangoObjectType):
    class Meta:
        model = Track  #class TrackType Inherites the Track Model


class LikeType(DjangoObjectType):
    class Meta:
        model = Like

class Query(graphene.ObjectType):
    tracks = graphene.List(TrackType,search=graphene.String())
    likes = graphene.List(LikeType)

    def resolve_tracks(self,info,search=None):
        if search:
            #Searches based on title.
            #To search based on multiple fields we use Q object
            filter = (
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(url__icontains=search) |
                Q(posted_by__username__icontains=search)
            )
            return  Track.objects.filter(filter)  #case insensitive i
        return Track.objects.all()  # returns all the tracks

    def resolve_likes(self,info):
        return  Like.objects.all()

class CreateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()

    def mutate(self, info, title, description, url):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Login to a track')

        track = Track(title=title,description=description,url=url, posted_by=user)
        track.save()
        return CreateTrack(track=track)

class UpdateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        track_id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()

    def mutate(self,info,track_id, title, description, url):
        user = info.context.user
        track = Track.objects.get(id=track_id)
        if track.posted_by != user:
            raise GraphQLError("Not permitted to update the track")

        track.title = title
        track.description = description
        track.url = url

        track.save()
        return UpdateTrack(track=track)


class DeleteTrack(graphene.Mutation):
    track_id = graphene.Int()

    class Arguments:
        track_id = graphene.Int(required=True)

    def mutate(self,info,track_id):
        user = info.context.user
        track = Track.objects.get(id=track_id)

        if track.posted_by != user:
            raise GraphQLError("Not permitted to delete the track")

        track.delete()

        return  DeleteTrack(track_id = track_id)

class CreateLike(graphene.Mutation):
    user = graphene.Field(UserType)
    track = graphene.Field(TrackType)

    class Arguments:
        track_id = graphene.Int(required=True)

    def mutate(self,info,track_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Login to like Tracks")

        track = Track.objects.get(id=track_id)
        if not track:
            raise GraphQLError("Cannot find the track with given track_id")

        Like.objects.create(
            user = user,
            track = track
        )

        return  CreateLike(user=user, track=track)

#Base Mutation Class
class Mutation(graphene.ObjectType):
    create_track = CreateTrack.Field()
    update_track = UpdateTrack.Field()
    delete_track = DeleteTrack.Field()
    create_like = CreateLike.Field()
