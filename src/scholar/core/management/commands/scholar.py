import textwrap
from itertools import zip_longest

import inquirer
from django.core.management.base import BaseCommand
from django.db.models import Q

from scholar.core.models import Card, Topic


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

    def add_card(self):
        topic = self.get_topic(new_ok=True)

    def edit_card(self):
        topic = self.get_topic()

    def show_topic(self):
        topic = self.get_topic()
        for card in topic.cards.all():
            self.print_card(card)
        print("Backrefs:")
        for card in topic.backrefs.all():
            self.print_card(card, with_topic=True)
        action = inquirer.list_input(
            message="What do you want to do?",
            choices=[
                ("Delete topic", "delete_topic"),
                ("Edit topic", "edit_topic"),
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
