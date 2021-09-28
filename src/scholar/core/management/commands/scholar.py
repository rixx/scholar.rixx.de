import textwrap
from itertools import zip_longest

import inquirer
from django.core.management.base import BaseCommand
from django.db.models import Q

from scholar.core.models import Card, Topic

SEPARATOR = "-+--+-\n"


class Command(BaseCommand):
    help = "Use scholar.rixx.de from the shell"

    def handle(self, *args, **options):
        while True:
            action = inquirer.list_input(
                message="What do you want to do?",
                choices=[
                    ("New card", "add_card"),
                    ("Edit a card", "edit_card"),
                    ("Show a topic", "show_topic"),
                    ("quit", "quit"),
                ],
                carousel=True,
            )
            if action == "quit":
                break
            getattr(self, action)()

    def get_topic(self, new_ok=False):
        while True:
            if new_ok:
                action = inquirer.list_input(
                    "What do you want to do?",
                    [
                        ("Find a topic", "find_topic"),
                        ("Add a new topic", "new_topic"),
                    ],
                    carousel=True,
                )
                if action == "new_topic":
                    return self._create_topic()
            search = inquirer.text("Topic search")
            topics = Topic.objects.filter(
                Q(title_en__icontains=search) | Q(title_de__icontains=search)
            )
            result = inquirer.list_input(
                message=">",
                choices=[
                    (f"{topic.title_en} / {topic.title_de}", topic) for topic in topics
                ]
                + [("None of these", None)],
                carousel=True,
            )
            if result:
                return result

    def _create_topic(self):
        title_en = inquirer.text("English title")
        title_de = inquirer.text("English title")
        return Topic.objects.create(title_en=title_en, title_de=title_de)

    def add_card(self, topic=None):
        if not topic:
            topic = self.get_topic(new_ok=True)
        text_en, text_de = inquirer.editor("", default=SEPARATOR).split(SEPARATOR)
        card = Card.objects.create(text_de=text_de, text_en=text_en, topic=topic)
        card.update_references()
        action = inquirer.list_input(
            message="What do you want to do?",
            choices=[
                ("Add another card", "new_card"),
                ("Continue", None),
            ],
            carousel=True,
        )
        if not action:
            return card
        return self.add_card(topic=topic)

    def select_card(self, topic):
        def card_text(card, backref=False):
            content = textwrap.shorten(card.text_en, width=40, placeholder="…")
            if not backref:
                return content
            return f"[Backref from {card.topic.title_en}] {content}"

        return inquirer.list_input(
            message="",
            choices=[(card_text(card), card) for card in topic.cards.all()]
            + [(card_text(card, backref=True), card) for card in topic.backrefs.all()],
        )

    def edit_card(self, topic=None):
        if not topic:
            topic = self.get_topic()
        card = self.select_card(topic)
        SEPARATOR = "-+--+-\n"
        card.text_en, card.text_de = inquirer.editor(
            "", default=f"{card.text_en}\n\n{SEPARATOR}\n\n{card.text_de}"
        ).split(SEPARATOR)
        card.text_en = card.text_en.strip()
        card.text_de = card.text_de.strip()
        card.save()
        card.update_references()
        action = inquirer.list_input(
            message="What do you want to do?",
            choices=[
                ("Edit another card on this topic", "edit_card"),
                ("Continue", None),
            ],
            carousel=True,
        )
        if not action:
            return card
        return self.edit_card(topic=topic)

    def show_topic(self):
        topic = self.get_topic()
        self.print_topic(topic)
        action = inquirer.list_input(
            message="What do you want to do?",
            choices=[
                ("Delete topic", "delete_topic"),
                ("Edit topic title", "edit_topic"),
                ("Edit a card", "edit_card"),
                ("Add a card", "new_card"),
                ("Continue", None),
            ],
            carousel=True,
        )
        if not action:
            return topic
        if action == "delete_topic":
            backrefs = topic.backrefs.all()
            topic.delete()
            for card in backrefs:
                card.update_references()
        elif action == "edit_topic":
            topic.title_en = inquirer.text("English title", default=topic.title_en)
            topic.title_de = inquirer.text("English title", default=topic.title_de)
            topic.save()
        elif action == "edit_card":
            self.edit_card(topic=topic)
        elif action == "add_card":
            self.add_card(topic=topic)

    def print_topic(self, topic):
        for card in topic.cards.all():
            self.print_card(card)
        print("Backrefs:")
        for card in topic.backrefs.all():
            self.print_card(card, with_topic=True)

    def print_card(self, card, width=70, buffer=6, with_topic=False):
        def line(text_left, text_right, align="left"):
            b = " " * int(buffer / 2)
            buffer_left = (width - len(text_left)) * " "
            buffer_right = (width - len(text_right)) * " "
            if align == "left":
                text_left = text_left + buffer_left
                text_right = text_right + buffer_right
            else:
                text_left = buffer_left + text_left
                text_right = buffer_right + text_right
            print(f"┃{b}{text_left}{b}┃{b}{text_right}{b}┃")

        text_en = textwrap.wrap(card.text_en, width=width)
        text_de = textwrap.wrap(card.text_de, width=width)
        print("┏" + "━" * (width + buffer) + "┳" + "━" * (width + buffer) + "┓")
        line("", "")
        for left, right in zip_longest(text_en, text_de, fillvalue=""):
            line(left, right)
        if with_topic:
            line("", "")
            line(card.topic.title_en, card.topic.title_de, align="right")
        line("", "")
        print("┗" + "━" * (width + buffer) + "┻" + "━" * (width + buffer) + "┛")
