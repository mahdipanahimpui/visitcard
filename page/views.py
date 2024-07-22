from django.shortcuts import render

# Create your views here.
from rest_framework import generics, mixins
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import PermissionDenied

from page.models import(
    Page,
    Image
)

from page.paginations import(
    PagePagination
)

from .serializers import(
    PageRetrieveSerializer,
    PageUpdateDestroySerializer,
    PageCreateSerializer, 
    PageListSerializer,

    ImageSerializer
)


# -------------------------------------------------------------------------
class UpdateDestroyAPIView(mixins.UpdateModelMixin,
                                   mixins.DestroyModelMixin,
                                   GenericAPIView):
    """
    Concrete view for updating or deleting a model instance.
    """

    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# ---------------------------------------------------------------------------------
class PageRetrieveView(generics.RetrieveAPIView):
    permission_classes = []
    serializer_class = PageRetrieveSerializer
    queryset = Page.objects.all()

    def get_object(self):
        obj = super().get_object()

        print('#'*90)
        print(self.request.user) # TODO: checking the request.user value

        if self.request.user != obj.user:
            print(obj.is_active_by_user)
            if not obj.is_active_by_user:
                raise PermissionDenied('the page is deactivated by page owner')
            if not obj.is_active_by_admin:
                raise PermissionDenied('the page is deactivated by superadmin')
        return obj
    

# ---------------------------------------------------------------------------------
class PageCreateView(generics.CreateAPIView):
    serializer_class = PageCreateSerializer
    queryset = Page.objects.all()


# ---------------------------------------------------------------------------------
class PageListView(generics.ListAPIView):
    serializer_class = PageListSerializer
    queryset = Page.objects.all()

    def get_object(self):
        obj = super().get_object()

        print('#'*90)
        print(self.request.user) # TODO: checking the request.user value

        if not obj.publish == 'private':
            raise PermissionDenied('the page is private.')
        
        if not obj.is_active_by_user:
            raise PermissionDenied('the page is deactivated by page owner.')
        
        if not obj.is_active_by_admin:
            raise PermissionDenied('the page is deactivated by superadmin.')
        
        return obj


# ---------------------------------------------------------------------------------
class PageUpdateView(generics.UpdateAPIView):
    pagination_class = PagePagination
    serializer_class = PageUpdateDestroySerializer
    queryset = Page.objects.all()

    def get_object(self):
        obj = super().get_object()

        print('#'*90)
        print(self.request.user) # TODO: checking the request.user value

        if self.request.user != obj.user:
                raise PermissionDenied('just owner has permission.')
        return obj


# ---------------------------------------------------------------------------------
class PageDestroyView(generics.DestroyAPIView):
    serializer_class = PageUpdateDestroySerializer
    queryset = Page.objects.all()

    def get_object(self):
        obj = super().get_object()

        print('#'*90)
        print(self.request.user) # TODO: checking the request.user value

        if self.request.user != obj.user:
                raise PermissionDenied('just owner has permission.')
        return obj


# ----------------------------------------------------------------------------------
class ImageCreateListView(generics.ListCreateAPIView):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()


    def get_queryset(self):
        page_id = self.kwargs.get('page_id', None)

        if (page_id is not None) and Page.objects.filter(id=page_id).exists():
            queryset = Image.objects.select_related('page').filter(page__id=page_id)
        else:  
            raise NotFound(f'page with id: {page_id} not found')
        return queryset

    

class ImageRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()

    def get_object(self):
        image_id = self.kwargs.get('image_id', None)

        if image_id is not None:
            obj = get_object_or_404(Image, id=image_id)
        else:
            raise NotFound(f'image with id: {image_id} not found')

        return obj




