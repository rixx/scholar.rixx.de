from rest_framework import serializers

from scholar.core.models import Card, Source, Tag, Topic


class FirstCardSerializer(serializers.ModelSerializer):
    """Used in flat topic views"""

    class Meta:
        model = Card
        fields = (
            "id",
            "text",
            "topic",
            "sources",
            "references",
            "prediction_deadline",
            "prediction_result",
        )


class FlatTopicSerializer(serializers.ModelSerializer):
    """Used in card view and nested card view within source view, plus in the search."""

    class Meta:
        model = Topic
        fields = ("id", "title", "info_box", "language", "translation")


class TopicFirstCardSerializer(serializers.ModelSerializer):
    """Used in tag view"""

    first_card = serializers.SerializerMethodField()

    def get_first_card(self):
        return FirstCardSerializer(self.first_card).data

    class Meta:
        model = Topic
        fields = (
            "id",
            "title",
            "info_box",
            "language",
            "translation",
            "first_card",
        )


class TagSerializer(serializers.ModelSerializer):
    topics = TopicFirstCardSerializer(many=True, read_only=True)

    class Meta:
        model = Tag
        fields = ("id", "name", "topics")


class FlatTagSerializer(serializers.ModelSerializer):
    """Used in the search."""

    class Meta:
        model = Tag
        fields = ("id", "name")


class SourceCardSerializer(FirstCardSerializer):
    topic = FlatTopicSerializer()

    class Meta:
        model = Card
        fields = ("id", "text", "topic", "prediction_deadline", "prediction_result")


class SourceSerializer(serializers.ModelSerializer):
    cards = SourceCardSerializer(many=True, required=False)

    class Meta:
        model = Source
        fields = ("id", "title", "url", "trust", "cards", "author", "notes")


class FlatSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ("id", "title", "url", "trust", "cards", "author", "notes")


class CardSerializer(serializers.ModelSerializer):
    topic = FlatTopicSerializer(read_only=False, required=False)
    sources = FlatSourceSerializer(read_only=False, many=True, required=False)
    references = FlatTopicSerializer(read_only=True, many=True, required=False)

    class Meta:
        model = Card
        fields = (
            "id",
            "text",
            "topic",
            "prediction_deadline",
            "prediction_result",
            "sources",
            "references",
        )


class CardWriteSerializer(serializers.ModelSerializer):
    topic = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Topic.objects.all(), required=False
    )
    sources = serializers.PrimaryKeyRelatedField(
        read_only=False, many=True, queryset=Source.objects.all(), required=False
    )

    def update(self, instance, validated_data):
        sources = validated_data.pop("sources", [])
        # old_instance = Card.objects.get(pk=instance.pk)  # TODO we will need this later on
        instance = super().update(instance, validated_data)
        instance.sources.set(sources)
        instance.update_references()
        return instance

    def create(self, validated_data):
        sources = validated_data.pop("sources", None)
        instance = Card.objects.create(**validated_data)
        if sources:
            instance.sources.set(sources)
        instance.update_references()
        return instance

    class Meta:
        model = Card
        fields = (
            "id",
            "text",
            "topic",
            "prediction_deadline",
            "prediction_result",
            "sources",
        )


class TopicSerializer(serializers.ModelSerializer):
    cards = CardSerializer(
        many=True, required=False
    )  # Duplicates topic info, we don't care for now
    backrefs = CardSerializer(
        many=True, required=False
    )  # Duplicates topic info, which we need

    class Meta:
        model = Topic
        fields = (
            "id",
            "title",
            "info_box",
            "language",
            "translation",
            "cards",
            "backrefs",
        )
