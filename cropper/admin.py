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
    
    def render_change_form(
            self, request, context, add=False, change=False, form_url='',
            obj=None):
        if obj is not None:
            context['image_to_crop'] = obj.source.image
        return super(CroppedImageAdmin, self).render_change_form(
            request, context, add=add, change=change, form_url=form_url,
            obj=obj
        )

admin.site.register(CroppedImage, CroppedImageAdmin)
