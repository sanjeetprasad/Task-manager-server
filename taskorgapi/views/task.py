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
        category_id = self.request.query_params.get("category_id", None)
        if category_id is not None:
            tasks = tasks.filter(category__id=category_id)
      
        serializer = TasksSerializer(
            tasks, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=[ 'post', 'delete'], detail=True)
    def tag(self, request, pk=None):

        if request.method=="POST":
            
            task=Tasks.objects.get(pk=pk)
            tag=Tags.objects.get(pk=request.data["tagId"])
            try:
                task_tag = TaskTags.objects.get(task=task, tag=tag)
                return Response(
                    {'message': 'this tag is on the task.'},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            except TaskTags.DoesNotExist:    
                task_tag=TaskTags()
                task_tag.task=task
                task_tag.tag=tag
                task_tag.save()
                return Response({}, status=status.HTTP_201_CREATED)

        elif request.method=="DELETE":
            try:
                task=Tasks.objects.get(pk=pk)

            except Tasks.DoesNotExist:
                return Response(
                    {'message': 'Task does not exist.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                task=Tasks.objects.get(pk=pk)
                
                tag=Tags.objects.get(pk=request.data["tagId"])
                
                task_tag = TaskTags.objects.get(task=task, tag=tag)
                
                task_tag.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            except TaskTags.DoesNotExist:
                return Response(
                    {'message': 'tag is not on the task'},
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


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
                # Finds the task by the id provided by URL
            task = Tasks.objects.get(pk=pk)
            # Filters tags matching the task primary key via the Tag_task
            matching_tags = Tags.objects.filter(tags__task=task)
            # Joins the tags to the task object
            print(matching_tags.query)
            task.tags=matching_tags


            serializer = Task_w_TagSerializer(task, context={'request': request}) 
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
        depth = 1

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ('id', 'label')
    
class Task_w_TagSerializer(serializers.ModelSerializer):
    """ Serializer to Join Task and Tags """
    # Defines the 'tags' field in the Serializer
    tags = TagSerializer(many=True)
    category = CategorySerializer(many=False)
    class Meta:
        model = Tasks
        fields = ('id', 'user', 'category', 'create_date_time', 'title', 'description', 'due_date_time', 'tags')
        depth = 2