from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Instruction(Page):
    def is_displayed(self):
        if self.round_number == 1:
           return True
        else:
           return False


class Contribute_first_page(Page):
      form_model = "player"
      form_fields = ["extraction"]




class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoff'

class Results(Page):
    pass




class Questionaire(Page):
    form_model = "player"
    form_fields = ["age,gender,income"]

    def is_displayed(self):
        if self.round_number == 6:
            return True
        else:
            return False




page_sequence = [Instruction, Contribute_first_page, ResultsWaitPage, Results, Questionaire]
