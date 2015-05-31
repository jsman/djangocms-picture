import os

from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin, Page
try:
    from cms.models import get_plugin_media_path
except ImportError:
    def get_plugin_media_path(instance, filename):
        """
        See cms.models.pluginmodel.get_plugin_media_path on django CMS 3.0.4+ for information
        """
        return instance.get_media_path(filename)
from cms.utils.compat.dj import python_2_unicode_compatible


@python_2_unicode_compatible
class Picture(CMSPlugin):
    """
    A Picture with or without a link.
    """
    LEFT = "left"
    RIGHT = "right"
    CENTER = "center"
    FLOAT_CHOICES = ((LEFT, _("left")),
                     (RIGHT, _("right")),
                     (CENTER, _("center")),
                     )
    STYLE_CHOICES = getattr(settings, 'DJANGOCMS_PICTURE_STYLES', None)

    image = models.ImageField(_("image"), upload_to=get_plugin_media_path)
    url = models.CharField(
        _("link"), max_length=255, blank=True, null=True,
        help_text=_("If present, clicking on image will take user to link."))

    page_link = models.ForeignKey(
        Page, verbose_name=_("page"), null=True,
        limit_choices_to={'publisher_is_draft': True}, blank=True,
        help_text=_("If present, clicking on image will take user to "
                    "specified page."))

    alt = models.CharField(
        _("alternate text"), max_length=255, blank=True, null=True,
        help_text=_("Specifies an alternate text for an image, if the image"
                    "cannot be displayed.<br />Is also used by search engines"
                    "to classify the image."))

    longdesc = models.CharField(
        _("long description"), max_length=255, blank=True, null=True,
        help_text=_("When user hovers above picture, this text will appear "
                    "in a popup."))

    float = models.CharField(
        _("side"), max_length=10, blank=True, null=True, choices=FLOAT_CHOICES,
        help_text=_("Move image left, right or center."))

    style = models.CharField(
        _("style"), max_length=255, blank=True, null=True, choices=STYLE_CHOICES,
        help_text=_("Select an optional image style."))

    is_responsive = models.BooleanField(_("Responsive"), default=False,
        help_text=_("Add Twitter Bootstrap `img-responsive` css class."))

    def __str__(self):
        if self.alt:
            return self.alt[:40]
        elif self.image:
            # added if, because it raised attribute error when file wasn't
            # defined.
            try:
                return u"%s" % os.path.basename(self.image.name)
            except AttributeError:
                pass
        return u"<empty>"

    def clean(self):
        if self.url and self.page_link:
            raise ValidationError(
                _("You can enter a Link or a Page, but not both."))
