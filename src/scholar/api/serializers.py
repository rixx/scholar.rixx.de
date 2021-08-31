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
    """Used in card view and nested card view within source view"""

    class Meta:
        model = Topic
        fields = ("id", "title", "slug", "info_box", "language", "translation")


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
            "slug",
            "info_box",
            "language",
            "translation",
            "first_card",
        )


class TagSerializer(serializers.ModelSerializer):
    topics = TopicFirstCardSerializer(many=True, read_only=True)

    class Meta:
        model = Tag
        fields = ("id", "name", "slug", "topics")


class SourceCardSerializer(FirstCardSerializer):
    topic = FlatTopicSerializer()

    class Meta:
        model = Card
        fields = ("id", "text", "topic", "prediction_deadline", "prediction_result")


class SourceSerializer(serializers.ModelSerializer):
    cards = SourceCardSerializer(many=True)

    class Meta:
        model = Source
        fields = ("id", "title", "url", "trust", "cards")


class FlatSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ("id", "title", "url", "trust", "cards")


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


class TopicFirstCardSerializer(serializers.ModelSerializer):
    """Used in card view and nested card view within source view"""

    cards = CardSerializer(many=True)  # Duplicates topic info, we don't care for now

    class Meta:
        model = Topic
        fields = (
            "id",
            "title",
            "slug",
            "info_box",
            "language",
            "translation",
            "first_card",
        )
