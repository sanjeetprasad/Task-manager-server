"""View module for handling requests about tasks"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from taskorgapi.models import Tags, Tasks, Categories, TaskTags
from rest_framework.decorators import action


class TasksView(ViewSet):


    def list(self, request):
        #Handles get all posts from the database

        tasks = Tasks.objects.filter(user= request.auth.user)
      
        serializer = TasksSerializer(
            tasks, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        
        task_user = User.objects.get(pk=request.auth.user.id)

        task = Tasks()
        task.title = request.data["title"]
        task.description = request.data["description"]
        task.create_date_time = request.data["createDateTime"]
        task.due_date_time = request.data["dueDateTime"]
        task.user = task_user

        category = Categories.objects.get(pk=request.data["categoryId"])

        task.category = category

        try:
            task.save()
            serializer = TasksSerializer(task, context={'request': request})
            return Response(serializer.data)
        
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single task

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            task = Tasks.objects.get(pk=pk)
            task.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def retrieve(self, request, pk=None):
        """Handle GET requests for single task

        Returns:
            Response -- JSON serialized post instance
        """

        try: 
            # Finds the post by the id provided by URL
            task = Tasks.objects.get(pk=pk)
            # Filters tags matching the post primary key via the Tag_Post
            # matching_tags = Tag.objects.filter(tags__post=post)
            # Joins the tags to the post object
            # print(matching_tags.query)
            # post.tags=matching_tags


            serializer = TasksSerializer(task, context={'request': request}) 
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def update(self, request, pk=None):
        # user = Rareuser.objects.get(user=request.auth.user)
        task_user = User.objects.get(pk=request.auth.user.id)

        task = Tasks.objects.get(pk=pk)
        task.title = request.data["title"]
        task.description = request.data["description"]
        task.create_date_time = request.data["createDateTime"]
        task.due_date_time = request.data["dueDateTime"]

        task.user = task_user

        category = Categories.objects.get(pk=request.data['categoryId'])
        task.category = category
        
        task.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tags
        fields = ('id', 'label')

class TasksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tasks
        fields = ( 'id', 'user', 'category', 'create_date_time', 'title', 'description', 'due_date_time' )


class Task_w_TagSerializer(serializers.ModelSerializer):
    """ Serializer to Join Post and Tags """
    # Defines the 'tags' field in the Serializer
    tags = TagSerializer(many=True)

    class Meta:
        model = Tasks
        fields = ('id', 'user', 'category', 'create_date_time', 'title', 'description', 'due_date_time', 'tags')
        