from rest_framework import serializers
from rest_framework.exceptions import ValidationError



from page.models import (
    Page,
    Image,
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
            'created_at',
            'updated_at'
        ]

        read_only_fields = [*base_read_only_fields, 'publish', 'slug', 'is_active_by_admin',
                            'is_active_by_user',
                            'is_premium', 'max_address_count', 
                            'max_image_count', 'max_comminucation_count']
        

# -------------------------------------------------------------------------------
class PageCreateSerializer(serializers.ModelSerializer):

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
            'created_at',
            'updated_at',
        ]

        read_only_fields = [*base_read_only_fields, 'slug']


# -------------------------------------------------------------------------------
class PageUpdateDestroySerializer(serializers.ModelSerializer):
    
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
            'created_at',
            'updated_at'
        ]

        read_only_fields = [*base_read_only_fields]


    def validate(self, attrs):
        if attrs.get('identification', None):
            attrs['slug'] = attrs['identification']
        return super().validate(attrs)


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
        print('page_'*20)
        print(page)

        max_image_count = page.max_image_count
        currnet_image_count = Image.objects.filter(page=page).count()

        if (page is not None) and (not currnet_image_count <= max_image_count):
            raise ValidationError(f'max_image_count: {max_image_count}, but current_image_count: {currnet_image_count}')
        
        return validation

        


