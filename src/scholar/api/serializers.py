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
        return FirstCardSerializer(self.first_card)

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
    topic = FlatTopicSerializer(read_only=False)
    sources = FlatSourceSerializer(read_only=False, many=True)
    references = FlatTopicSerializer(read_only=True, many=True)

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


class TopicSerializer(serializers.ModelSerializer):
    cards = CardSerializer(
        many=True, required=False
    )  # Duplicates topic info, we don't care for now

    class Meta:
        model = Topic
        fields = (
            "id",
            "title",
            "info_box",
            "language",
            "translation",
            "first_card",
            "cards",
        )
