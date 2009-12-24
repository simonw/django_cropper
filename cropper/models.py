from django.db import models
from django.core.files.base import ContentFile
from StringIO import StringIO
import Image, uuid

class SourceImage(models.Model):
    name = models.CharField(max_length = 255, blank = True)
    description = models.TextField(blank = True)
    image = models.ImageField(
        upload_to='sources/%Y/%m', blank = True, max_length=255
    )
    preview = models.ImageField(
        upload_to='preview/%Y/%m', blank = True, max_length=255, editable=0
    )
    url = models.URLField(verify_exists = False, blank = True)
    
    def save(self, *args, **kwargs):
        if self.image:
            original = Image.open(self.image)
            if original.size[0] > 800:
                print(800, int(original.size[1] * (800.0 / original.size[0])))
                preview = original.resize(
                    (800, int(original.size[1] * (800.0 / original.size[0])))
                )
            else:
                preview = original.resize(original.size)
            
            contents = StringIO()
            preview.save(contents, format='jpeg', quality=25)
            self.preview.save(
                '%s.jpg' % str(uuid.uuid4()),
                ContentFile(contents.getvalue()), save=False
            )
        super(SourceImage, self).save(*args, **kwargs)
    
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
            if self.size:
                cropped = cropped.resize(
                    (self.size.width, self.size.height), Image.ANTIALIAS
                )
            contents = StringIO()
            cropped.save(contents, format='jpeg', quality=90)
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
