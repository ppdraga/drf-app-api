from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe
from recipe import serializers


class BaseRecipeAttrViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        '''Return objects for the current authenticated user only'''
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        '''Create new tag'''
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()


class RecipeViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()

    def _params_to_ints(self, str_param):
        return [int(str_val) for str_val in str_param.split(',')]

    def get_queryset(self):
        '''Return objects for the current authenticated user only'''
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        qs = self.queryset
        if tags:
            qs = qs.filter(tags__id__in=self._params_to_ints(tags))
        if ingredients:
            qs = qs.filter(ingredients__id__in=self._params_to_ints(ingredients))
        return qs.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        recipe = self.get_object()
        serializer = self.get_serializer(
            recipe,
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
