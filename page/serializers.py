from rest_framework import serializers
from rest_framework.exceptions import ValidationError



from page.models import (
    Page,
    Image,
    Comminucation,
    Address,
    Location
)


base_read_only_fields = [
    'id', 'created_at', 'updated_at'
]

# --------------------------------------------------------------------------
class PageRetrieveSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Page

        fields = [
            'id',
            'user',
            'identification',
            'title',
            'subject',
            'description',
            'max_address_count',
            'max_image_count',
            'max_comminucation_count',
            'publish',
            'slug', 
            'is_active_by_admin',
            'is_active_by_user',
            'is_premium',
            'expire_datetime',
            'created_at',
            'updated_at'
        ]

        read_only_fields = [*base_read_only_fields, 'publish', 'slug', 'is_active_by_admin',
                            'is_active_by_user', 'expire_datetime',
                            'is_premium', 'max_address_count', 
                            'max_image_count', 'max_comminucation_count']
        

# -------------------------------------------------------------------------------
class PageCreateUpdateDestroySerializer(serializers.ModelSerializer):

    class Meta:
        model = Page

        fields = [
            'id',
            'user',
            'identification',
            'title',
            'subject',
            'description',
            'max_address_count',
            'max_image_count',
            'max_comminucation_count',
            'publish',
            'slug',
            'cv',
            'is_active_by_admin',
            'is_active_by_user',
            'is_premium',
            'expire_datetime',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [*base_read_only_fields, 'slug', 'max_address_count', 'expire_datetime'
                            'max_image_count', 'max_comminucation_count', 'is_active_by_admin', 'is_premium']


# -------------------------------------------------------------------------------
# class PageUpdateDestroySerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Page

#         fields = [
#             'id',
#             'user',
#             'identification',
#             'title',
#             'subject',
#             'description',
#             'max_address_count',
#             'max_image_count',
#             'max_comminucation_count',
#             'publish',
#             'slug', 
#             'cv',
#             'is_active_by_admin',
#             'is_active_by_user',
#             'is_premium',
#             'created_at',
#             'updated_at'
#         ]

#         read_only_fields = [*base_read_only_fields]


# -------------------------------------------------------------------------------
class PageListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Page

        fields = [
            'id',
            'user',
            'identification',
            'title',
            'subject',
            'slug', 
            'created_at',
            'updated_at'
        ]

        read_only_fields = [*base_read_only_fields]



# ---------------------------------------------------------------------------------
class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model : Image
        fields = '__all__'

        read_only_fields = [*base_read_only_fields]


    def validate(self, attrs):
        validation = super().validate(attrs)
        page = attrs.get('page', None)

        if page:

            max_image_count = page.max_image_count
            currnet_image_count = Image.objects.filter(page=page).count()

            if self.context['request'].method == 'PUT':
                currnet_image_count += 1

            if not currnet_image_count <= max_image_count:
                raise ValidationError(f'max_image_count: {max_image_count}, current_image_count: {currnet_image_count}')

        return validation
    


# ---------------------------------------------------------------------------------
class ComminucationSerializer(serializers.ModelSerializer):

    class Meta:
        model : Comminucation
        fields = '__all__'
        read_only_fields = [*base_read_only_fields]



    def validate(self, attrs):
        validation = super().validate(attrs)
        page = attrs.get('page', None)

        if page:

            max_comminucation_count = page.max_comminucation_count
            currnet_comminucation_count = Comminucation.objects.filter(page=page).count()

            if self.context['request'].method == 'PUT':
                currnet_comminucation_count += 1

            if not currnet_comminucation_count < max_comminucation_count:
                raise ValidationError(f'max_comminucation_count: {max_comminucation_count}, currnet_comminucation_count: {currnet_comminucation_count}')
            
        return validation
    

# ---------------------------------------------------------------------------------
class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model : Address
        fields = '__all__'
        read_only_fields = [*base_read_only_fields]


    def validate(self, attrs):
        validation = super().validate(attrs)
        page = attrs.get('page', None)

        if page:

            max_address_count = page.max_address_count
            currnet_address_count = Address.objects.filter(page=page).count()

            if self.context['request'].method == 'PUT':
                currnet_address_count += 1

            if not currnet_address_count < max_address_count:
                raise ValidationError(f'max_address_count: {max_address_count}, currnet_address_count: {currnet_address_count}')
            
        return validation
    


# ---------------------------------------------------------------------------------
class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model : Location
        fields = '__all__'
        read_only_fields = [*base_read_only_fields]


    def validate(self, attrs):
        validation = super().validate(attrs)
        page = attrs.get('page', None)

        if page:

            max_location_count = page.max_location_count
            currnet_location_count = Location.objects.filter(page=page).count()

            if self.context['request'].method == 'PUT':
                currnet_location_count += 1

            if not currnet_location_count < max_location_count:
                raise ValidationError(f'max_location_count: {max_location_count}, currnet_location_count: {currnet_location_count}')
            
        return validation
    

        


