import re
import uuid

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.functional import cached_property
from ordered_model.models import OrderedModel
from rest_framework.authtoken.models import Token

REFERENCE_REGEX = r"(?<=\[\[).*?(?=(?:\]\]|#|\|))"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class BaseModel(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Topic(BaseModel):
    """A Topic is a collection of cards, with a bit of metadata of its own.

    Most of the metadata is calculated from cards – both its own and
    related ones.
    """

    title_de = models.CharField(max_length=100)
    title_en = models.CharField(max_length=100)

    info_box = models.JSONField(null=True, blank=True)
    tags = models.ManyToManyField("Tag", related_name="topics")

    @cached_property
    def sources(self):
        return Source.objects.filter(cards__topic=self)

    @cached_property
    def first_card(self):
        # TODO use annotation if present
        return self.cards.all().first()


class Card(OrderedModel, BaseModel):
    """Cards don't have to have a topic: they can just belong to one source,
    until a proper topic is found or made."""

    text_de = models.TextField()
    text_en = models.TextField()
    topic = models.ForeignKey(
        to=Topic, on_delete=models.CASCADE, related_name="cards", null=True
    )
    sources = models.ManyToManyField(
        "Source", through="CardSourceThrough", related_name="cards"
    )
    references = models.ManyToManyField(
        Topic, through="CardTopicThrough", related_name="backrefs"
    )
    prediction_deadline = models.DateTimeField(null=True, blank=True)
    prediction_result = models.BooleanField(null=True, blank=True)

    order_with_respect_to = "topic"

    class Meta(OrderedModel.Meta):
        pass

    def update_references(self):
        references_en = list(re.findall(REFERENCE_REGEX, self.text_en))
        references_de = list(re.findall(REFERENCE_REGEX, self.text_de))
        references_obj = set()
        if len(references_de) == len(references_en):
            # we can be clever here
            # and by "clever" I mean that everything is still terrible
            # but within the constraints of the data model, we can be clever
            for word_en, word_de in zip(references_en, references_de):
                topic_en = Topic.objects.filter(title_en__iexact=word_en).first()
                topic_de = Topic.objects.filter(title_en__iexact=word_de).first()
                if topic_en and topic_de:
                    references_obj.add(topic_en)
                    references_obj.add(topic_de)
                elif not topic_en and not topic_de:
                    topic = Topic.objects.create(title_en=word_en, title_de=word_de)
                    references_obj.add(topic)
                elif topic_en:
                    references_obj.add(topic_en)
                    topic = Topic.objects.create(title_en=word_de, title_de=word_de)
                    references_obj.add(topic)
                else:
                    references_obj.add(topic_de)
                    topic = Topic.objects.create(title_en=word_en, title_de=word_en)
                    references_obj.add(topic)
        else:
            for word in references_en + references_de:
                topic = Topic.objects.filter(
                    Q(title_en__iexact=word) | Q(title_de__iexact=word)
                ).first()
                if not topic:
                    topic = Topic.objects.create(title_en=word, title_de=word)
                references_obj.add(topic)
        self.references.set(references_obj)
        return references_obj


class Source(BaseModel):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100, null=True, blank=True)
    notes_de = models.TextField(null=True, blank=True)
    notes_en = models.TextField(null=True, blank=True)
    url = models.URLField(max_length=200, null=True, blank=True)
    trust = models.IntegerField(
        choices=(
            (0, "incorrect"),
            (1, "probably incorrect"),
            (2, "who knows, 50/50 of being correct (pop sci)"),
            (3, "better than 50/50 at least (good pop sci)"),
            (4, "good source"),
            (5, "excellent source"),
        )
    )


class CardSourceThrough(OrderedModel):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    order_with_respect_to = "card"

    class Meta:
        ordering = ("card", "source")


class CardTopicThrough(OrderedModel):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    order_with_respect_to = "card"

    class Meta:
        ordering = ("card", "topic")


class Tag(BaseModel):
    name_en = models.CharField(max_length=50)
    name_de = models.CharField(max_length=50)
