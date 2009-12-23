from django.db import models
from django.core.files.base import ContentFile
from StringIO import StringIO
import Image

class SourceImage(models.Model):
    name = models.CharField(max_length = 255, blank = True)
    description = models.TextField(blank = True)
    image = models.ImageField(
        upload_to='sources/%Y/%m', blank = True, max_length=255
    )
    url = models.URLField(verify_exists = False, blank = True)
    
    def __unicode__(self):
        s = u''
        if self.name:
            s = u'%s: ' % self.name
        if self.image:
            s += self.image.url
        else:
            s += self.url
        return s

class CropSize(models.Model):
    name = models.CharField(max_length = 255, blank = True)
    description = models.TextField(blank = True)
    width = models.PositiveSmallIntegerField()
    height = models.PositiveSmallIntegerField()
    
    def __unicode__(self):
        if self.name:
            return u'%s: %sx%s' % (self.name, self.width, self.height)
        else:
            return u'%sx%s' % (self.width, self.height)

class CroppedImage(models.Model):
    source = models.ForeignKey(SourceImage)
    size = models.ForeignKey(CropSize, blank = True, null = True)
    x = models.PositiveSmallIntegerField(null = True, blank = True)
    y = models.PositiveSmallIntegerField(null = True, blank = True)
    w = models.PositiveSmallIntegerField(null = True, blank = True)
    h = models.PositiveSmallIntegerField(null = True, blank = True)
    needs_generating = models.BooleanField(default = True)
    image = models.ImageField(
        upload_to='crops/%Y/%m', blank = True, max_length=255
    )
    
    def save(self, *args, **kwargs):
        # Crop the image, provided x/y/w/h are available
        if self.x and self.y and self.w and self.h:
            original = Image.open(self.source.image)
            cropped = original.crop(
                # left, upper, right, lower
                (self.x, self.y, (self.x + self.w), (self.y + self.h))
            )
            contents = StringIO()
            cropped.save(contents, format='jpeg')
            self.image.save(
                '%s-%s-%s-%sx%s.jpg' % (self.pk,self.x,self.y,self.w,self.h),
                ContentFile(contents.getvalue()), save=False
            )
        super(CroppedImage, self).save(*args, **kwargs)
    
    def __unicode__(self):
        if self.image:
            return self.image.path
        else:
            return u'Crop of %s' % self.source.image.path
