
"""Category ViewSet and Serializers"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, serializers
from django.http.response import HttpResponseServerError
from taskorgapi.models import Categories

class CategoryView(ViewSet):
    """Categories view set"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized category instance
        """

        category = Categories()
        category.label = request.data["label"]

        try:
            category.save()
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """Handle GET requests to games resource

        Returns:
            Response -- JSON serialized list of categories
        """
        # Get all category records from the database
        categories = Categories.objects.all()


        serializer = CategorySerializer(
            categories, many=True, context={'request': request})
        return Response(serializer.data)

    def list(self,request):
        """GET a new Categories object"""
        categories = Categories.objects.all()
        serialized_categories = CategoriesSerializer(categories, many=True)
        return Response(serialized_categories.data, status=status.HTTP_200_OK)

    def update(self, reqeust, pk=None):
        # Handle PUT request for a category, return HTTP status code of 204 upon success
        category = Categories.objects.get(pk=pk)
        category.label = reqeust.data["label"]
        category.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

        # Handle HTTP DELETE method and return HTTP status code of 204, 404, or 500
    def destroy(self, request, pk=None):
        try:
            category = Categories.objects.get(pk=pk)
            category.delete()

            #return HTTP 204 to client if no errors
            return Response({}, status=status.HTTP_204_NO_CONTENT)

       # return HTTP 404 to client if label not found
        except Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
        # return HTTP 500 to client if exception is thrown
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CategoriesSerializer(serializers.ModelSerializer):
    """JSON serializer for categories"""
    class Meta:
        model = Categories
        fields = ('id', 'label')