from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Surveyquestion(Page):
    form_model = "player"
    form_fields =



page_sequence = [Surveyquestion]
