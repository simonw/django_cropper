from django.contrib import admin
from models import SourceImage, CropSize, CroppedImage

admin.site.register(SourceImage)
admin.site.register(CropSize)

class CroppedImageAdmin(admin.ModelAdmin):
    change_form_template = 'cropper/crop_admin_interface.html'
    
    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            fields = ('source', 'size')
        else:
            fields = ('source', 'size', 'x', 'y', 'w', 'h')
        kwargs['fields'] = fields
        return super(CroppedImageAdmin, self).get_form(request, obj, **kwargs)

admin.site.register(CroppedImage, CroppedImageAdmin)
