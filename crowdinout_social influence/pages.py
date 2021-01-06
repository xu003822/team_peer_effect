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
    #Display this page only if paricipant disagrees with the terms.
    def is_displayed(self):
        return self.player.consent == 0

class Instruction(Page):
    def is_displayed(self):
        if self.round_number == 1:
           return True
        else:
           return False

class Quiz(Page):
    form_model = 'player'
    form_fields = ['quiz1_all']
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

class Fine_Instruction(Page):
    def is_displayed(self):
       # if self.round_number == 4 and self.player.id_in_group == self.player.playeraudit: #only for the selected individual, the fine is shown
        if self.round_number == (Constants.num_rounds - 4)
           return True
        else:
           return False


class Revoke_Instruction(Page):

    def is_displayed(self):
        if self.round_number == (Constants.num_rounds - 2):
           return True
        else:
           return False


class Contribute_first_page(Page):
      form_model = "player"
      form_fields = ["extraction"]

      def is_displayed(self):
          if self.round_number != 1:
              return True
          else:
              return False

      def vars_for_template(self):
          round_numb = self.round_number - 1
          return dict(round_nm = round_numb) # it seems you have to put the variables in a dictionary which contains all variables you send to the template

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoff'

class ResultsPractice(Page):
    def is_displayed(self):
        if self.round_number == 1:
            return True
        else:
            return False

class Results(Page):
    def is_displayed(self):
        if self.round_number != 1:
            return True
        else:
            return False


class Questionaire(Page):
    form_model = "player"
    form_fields = ["age","gender","income"]

    def is_displayed(self):
        if self.round_number == 7:
            return True
        else:
            return False

class Final_Thank_you(Page):
    pass

page_sequence = [consent, Disagree, Instruction, Quiz, PracticeRound, Practice, Fine_Instruction, Revoke_Instruction, Contribute_first_page, ResultsWaitPage, ResultsPractice, Results, Questionaire, Final_Thank_you]
