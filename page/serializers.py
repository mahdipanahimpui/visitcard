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
            'num_of_addresses',
            'num_of_images',
            'num_of_comminucations',
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
                            'is_premium', 'num_of_addresses', 
                            'num_of_images', 'num_of_comminucations']
        

# -------------------------------------------------------------------------------
class PageCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child = serializers.ImageField(max_length=100000, allow_empty_file=False, use_url=False),
        required=False
    )

    class Meta:
        model = Page

        fields = [
            'id',
            'user',
            'identification',
            'title',
            'subject',
            'description',
            'num_of_addresses',
            'num_of_images',
            'num_of_comminucations',
            'publish',
            'slug',
            'cv',
            'is_active_by_admin',
            'is_active_by_user',
            'is_premium',
            'created_at',
            'updated_at',

            'images',
        ]

        read_only_fields = [*base_read_only_fields]

    def validate(self, data):
        print('in_createion')
        print('admin', data['is_active_by_admin'])
        print('user', data['is_active_by_user'])

        data['is_active_by_admin'] = data.get('is_active_by_admin', True)
        data['is_active_by_user'] = data.get('is_active_by_user', True)
        return super().validate(data)
    

    # def create_images(self, images, instance):
    #     for image in images:
    #         image_instance = Image.objects.create(image=image, page=instance)
    #         PageImageRelation.objects.create(image)
            


    # def create(self, validated_data):
    #     uploaded_images = validated_data.pop('images', [])
    #     validated_data.pop('image_ids_to_delete', [])
    #     instance = super().create(validated_data)
    #     # self.create_images(uploaded_images, instance)

    #     return instance
    


    # def update(self, instance, validated_data):
    #     uploaded_images = validated_data.pop('images', [])
    #     image_ids_to_delete = self.validated_data.pop('image_ids_to_delete', [])

    #     self.create_images(uploaded_images, page=instance)
        
    #     if image_ids_to_delete:
    #         self.delete_images(image_ids_to_delete, field_condition)

    #     return super().update(instance, validated_data)


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
            'num_comminucation_count',
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

        


