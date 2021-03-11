"""Category ViewSet and Serializers"""
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, serializers
from taskorgapi.models import Tasks, Tags, Categories, TaskTags
from django.contrib.auth.models import User


class TasksView(ViewSet):
    """Todo view set"""

    def list(self,request):
        """GET a Todo object"""
        app_user = User.objects.get(id=request.auth.user.id)

        tasks = Tasks.objects.filter(user_id=app_user)
        
        # e.g.: /todos?categories=1
        category_id = self.request.query_params.get('categories', None)
        if category_id is not None:
            tasks = tasks.filter(category_id=category_id)

        # e.g.: /todos?tags=1
    #first find the tag id the client wants to filter by
    #if tag is there then we need to find all todos that contain that tag in its tags array
        tag_id = self.request.query_params.get('tagId', None)
        if tag_id is not None:
            tasktags = TaskTags.objects.filter(tag_id=tag_id)
            tasks = [tasktag.task for tasktag in tasktags]
                    

        serialized_todos = TaskSerializer(tasks, many=True, context={'request': request})
        return Response(serialized_tasks.data, status=status.HTTP_200_OK)



# class TaskSerializer(serializers.ModelSerializer):
#     """JSON serializer for Task"""
#     user = UserSerializer(many=False)
#     category = CategoriesSerializer(many=False)
#     tags = TaskTagsSerializer(many=True)

#     class Meta:
#         model = Tasks
#         fields = ('id', 'user', 'category', 'create_date_time', 'title', 'description', 'due_date_time')
#         depth = 1