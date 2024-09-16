from django.shortcuts import render
from django.utils import timezone
# Create your views here.
from rest_framework import generics, mixins
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import PermissionDenied

from page.models import(
    Page,
    Image,
    Comminucation,
    Address, 
    Location
)

from page.paginations import(
    PagePagination
)

from .serializers import(
    PageRetrieveSerializer,
    PageCreateUpdateDestroySerializer,
    PageListSerializer,

    ImageSerializer,
    ComminucationSerializer,
    AddressSerializer,
    LocationSerializer
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

        if self.request.user != obj.user:

            if not obj.is_active_by_user:
                raise PermissionDenied('the page is deactivated by page owner')
            
            if not obj.is_active_by_admin:
                raise PermissionDenied('the page is deactivated by superadmin')
            
            print('@'*100)
            print('expire_datetme', obj.expire_datetime)
            print('now:', timezone.now())

            if not obj.expire_datetime <= timezone.now():
                raise PermissionDenied('the page is expired, charge it')

        return obj
    

# ---------------------------------------------------------------------------------
class PageCreateView(generics.CreateAPIView):
    serializer_class = PageCreateUpdateDestroySerializer
    queryset = Page.objects.all()


# ---------------------------------------------------------------------------------
class PageListView(Filtration, generics.ListAPIView):
    serializer_class = PageListSerializer
    queryset = Page.objects.all()

    # def get(self):
    #     obj = super().get_object()

    #     print('#'*90)
    #     print(self.request.user) # TODO: checking the request.user value

    #     if not obj.publish == 'private':
    #         raise PermissionDenied('the page is private.')
        
    #     if not obj.is_active_by_user:
    #         raise PermissionDenied('the page is deactivated by page owner.')
        
    #     if not obj.is_active_by_admin:
    #         raise PermissionDenied('the page is deactivated by superadmin.')
        
    #     return obj

    
    def get_queryset(self):
        queryset = super().get_queryset()
        now = timezone.now()
        queryset = queryset.filter(publish='public', is_active_by_user=True, is_active_by_admin=True, expire_datetime__lte=now)
        return queryset


# ---------------------------------------------------------------------------------
class PageUpdateView(generics.UpdateAPIView):
    serializer_class = PageCreateUpdateDestroySerializer
    queryset = Page.objects.all()

    def get_object(self):
        obj = super().get_object()

        # if self.request.user != obj.user:
        #         raise PermissionDenied('just owner has permission.')
        return obj


# ---------------------------------------------------------------------------------
class PageDestroyView(generics.DestroyAPIView):
    serializer_class = PageCreateUpdateDestroySerializer
    queryset = Page.objects.all()

    def get_object(self):
        obj = super().get_object()

        print('#'*90)
        print(self.request.user) # TODO: checking the request.user value

        # if self.request.user != obj.user:
        #         raise PermissionDenied('just owner has permission.')
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

    
 # ------------------------------------------------------------------------------------
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
    
# ----------------------------------------------------------------------------------
class ComminucationCreateListView(generics.ListCreateAPIView):
    serializer_class = ComminucationSerializer
    queryset = Address.objects.all()


    def get_queryset(self):
        page_id = self.kwargs.get('page_id', None)

        if (page_id is not None) and Page.objects.filter(id=page_id).exists():
            queryset = Comminucation.objects.select_related('page').filter(page__id=page_id)
        else:  
            raise NotFound(f'page with id: {page_id} not found')
        return queryset
    

 # ------------------------------------------------------------------------------------
class ComminucationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ComminucationSerializer
    queryset = Comminucation.objects.all()

    def get_object(self):
        comminucation_id = self.kwargs.get('comminucation_id', None)

        if comminucation_id is not None:
            obj = get_object_or_404(Comminucation, id=comminucation_id)
        else:
            raise NotFound(f'comminucation with id: {comminucation_id} not found')

        return obj
    

# ----------------------------------------------------------------------------------
class AddressCreateListView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()


    def get_queryset(self):
        page_id = self.kwargs.get('page_id', None)

        if (page_id is not None) and Page.objects.filter(id=page_id).exists():
            queryset = Address.objects.select_related('page').filter(page__id=page_id)
        else:  
            raise NotFound(f'page with id: {page_id} not found')
        return queryset
    

 # ------------------------------------------------------------------------------------
class AddressRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    def get_object(self):
        address_id = self.kwargs.get('address_id', None)

        if address_id is not None:
            obj = get_object_or_404(Address, id=address_id)
        else:
            raise NotFound(f'address_id with id: {address_id} not found')

        return obj


# ----------------------------------------------------------------------------------
class LocationCreateListView(generics.ListCreateAPIView):
    serializer_class = LocationSerializer
    queryset = Address.objects.all()


    def get_queryset(self):
        page_id = self.kwargs.get('page_id', None)

        if (page_id is not None) and Page.objects.filter(id=page_id).exists():
            queryset = Location.objects.select_related('page').filter(page__id=page_id)
        else:  
            raise NotFound(f'page with id: {page_id} not found')
        return queryset
    

 # ------------------------------------------------------------------------------------
class LocationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()

    def get_object(self):
        location_id = self.kwargs.get('location_id', None)

        if location_id is not None:
            obj = get_object_or_404(Location, id=location_id)
        else:
            raise NotFound(f'location_id with id: {location_id} not found')

        return obj


