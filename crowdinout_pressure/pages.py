from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class consent(Page):
    form_model = 'player'
    form_fields = ['consent']

    def is_displayed(self):
        if self.round_number == 1:
            return True
        else:
            return False


class Disagree(Page):
    # Display this page only if paricipant disagrees with the terms.
    def is_displayed(self):
        return self.player.consent == 0


class Instruction(Page):
    form_model = 'player'
    form_fields = ['id_number']

    def before_next_page(self):
        if self.round_number == 1:
           self.participant.vars['idnumber'] = self.player.id_number

    def is_displayed(self):
        if self.round_number == 1:
            return True
        else:
            return False


class Quiz(Page):
    form_model = 'player'
    form_fields = ['quiz1_all','quiz2_all']


    def is_displayed(self):
        if self.round_number == 1:
            return True
        else:
            return False


class PracticeRound(Page):
    def is_displayed(self):
        if self.round_number == 1:
            return True
        else:
            return False


class Practice(Page):
    form_model = "player"
    form_fields = ["extraction"]

    def is_displayed(self):
        if self.round_number == 1:
            return True
        else:
            return False

class Practice2(Page):
    form_model = "player"
    form_fields = ["extraction"]

    def is_displayed(self):
        if self.round_number == 2:
            return True
        else:
            return False

class socialpressure_Instruction(Page):
    def is_displayed(self):
        if self.round_number == (Constants.num_rounds - 4):
            return True
        else:
            return False


class Revoke_Instruction(Page):

    def is_displayed(self):
        if self.round_number == Constants.num_rounds-2:
            return True
        else:
            return False


class Contribute_first_page(Page):
    form_model = "player"
    form_fields = ["extraction"]

    def is_displayed(self):
        if self.round_number not in [1,2]:
            return True
        else:
            return False

    def vars_for_template(self):
        round_numb = self.round_number - 2

        return dict(
            round_nm=round_numb
            )  # it seems you have to put the variables in a dictionary which contains all variables you send to the template



class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoff'


class ResultsPractice(Page):
    def is_displayed(self):
        if self.round_number == 2:
            return True
        else:
            return False


class Results(Page):
    def is_displayed(self):
        if self.round_number not in [2, Constants.num_rounds - 3, Constants.num_rounds - 4]:
            return True
        else:
            return False

class Results_pressure(Page):
    def is_displayed(self):
        if self.round_number in [Constants.num_rounds - 3, Constants.num_rounds - 4]:
            return True
        else:
            return False


class Questionaire(Page):
    form_model = "player"
    form_fields = ["age", "gender", "income", "party"]

    def is_displayed(self):
        if self.round_number == Constants.num_rounds:
            return True
        else:
            return False


class Final_Thank_you(Page):
    def is_displayed(self):
        if self.round_number == Constants.num_rounds:
            return True
        else:
            return False


page_sequence = [consent, Disagree, Instruction, Quiz, PracticeRound, Practice, Practice2, socialpressure_Instruction, Revoke_Instruction,
                 Contribute_first_page, ResultsWaitPage, ResultsPractice, Results, Results_pressure, Questionaire, Final_Thank_you]
