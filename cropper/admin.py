from django.contrib import admin
from django.utils.safestring import mark_safe
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
    
    def preview_thumb(self, obj):
        if obj.image:
            return mark_safe(
                u'<img src="%s" style="width: 200px">' % obj.image.url
            )
        else:
            return None
    preview_thumb.allow_tags = True
    
    list_display = ('__unicode__', 'size', 'preview_thumb')
    list_filter = ('size',)

admin.site.register(CroppedImage, CroppedImageAdmin)
