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

class Quiz2_1(Page):
    form_model = 'player'
    form_fields = ['quiz3_all','quiz4_all']

    def is_displayed(self):
        if self.round_number == 1 & (self.participant.vars['quiz'] == 0):
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

class Fine_Instruction(Page):
    def is_displayed(self):
        if self.round_number == (Constants.num_rounds - 4):
            return True
        else:
            return False

    def vars_for_template(self):
        round_numb = self.round_number - 1

        return dict(
            round_nm=round_numb
            )

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
        if  self.round_number not in [1, 2, Constants.num_rounds - 3, Constants.num_rounds - 4]:
            return True
        else:
            return False

    def vars_for_template(self):
        round_numb = self.round_number - 2

        return dict(
            round_nm=round_numb
            )  # it seems you have to put the variables in a dictionary which contains all variables you send to the template

class Results_audited(Page):
    def is_displayed(self):
        #if the player gets audited and also the round is in the auditing round
        if (self.round_number in [Constants.num_rounds - 3, Constants.num_rounds - 4]) and self.player.audit_or_not == 1:
            return True
        else:
            return False


class Results_notaudited(Page):
    def is_displayed(self):
        #if the player does not get audited and also the round is in the auditing round
        if (self.round_number in [Constants.num_rounds - 3, Constants.num_rounds - 4]) and self.player.audit_or_not == 0:
            return True
        else:
            return False

class regulation_audit(Page):
    form_model = "player"
    form_fields = ["extraction"]

    def is_displayed(self):
        #if the player does not get audited and also the round is in the auditing round
        if  self.round_number in [Constants.num_rounds - 3, Constants.num_rounds - 4]:
            return True
        else:
            return False

    def vars_for_template(self):
        round_numb = self.round_number - 2

        return dict(
            round_nm=round_numb
            )

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoff'

class ResultsPractice(Page):
    def is_displayed(self):
        if self.round_number == 2:
            return True
        else:
            return False

class Results_noreg(Page):
    def is_displayed(self):
        if  self.round_number in [Constants.num_rounds - 3, Constants.num_rounds - 4] and self.player.audit_or_not == 2:
            return True
        else:
            return False

class Results(Page):
    def is_displayed(self):
        if  self.round_number not in [2, Constants.num_rounds - 3, Constants.num_rounds - 4]:
            return True
        else:
            return False
#(self.round_number not in [Constants.num_rounds - 3, Constants.num_rounds - 4]) or

class Questionaire(Page):
    form_model = "player"
    form_fields = ["age", "gender", "income", "party", "strategy", "strategy_repeal"]

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

page_sequence = [consent, Disagree, Instruction, Quiz, Quiz2_1, PracticeRound, Practice, Practice2, Fine_Instruction,
                 Revoke_Instruction, Contribute_first_page, regulation_audit, ResultsWaitPage, ResultsPractice, Results, Results_audited,
                 Results_notaudited, Results_noreg, Questionaire, Final_Thank_you]
