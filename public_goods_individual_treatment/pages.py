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

class ID(Page):
    form_model = 'player'
    form_fields = ['id_number']

    def is_displayed(self):
        if self.round_number == 1:
            return True
        else:
            return False

class Instruction(Page):

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
        if self.round_number == 1:
            return True
        else:
            return False


class Contribute_first_page(Page):
    form_model = "player"
    form_fields = ["contribution"]

    def is_displayed(self):
        if self.round_number == 1:
            return True
        else:
            return False

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoff'

    def is_displayed(self):
        if self.round_number <= 21:
            # before it is self.round_number <= 4:
            return True
        else:
            return False



class Results(Page):
    def is_displayed(self):
        if self.player.id_in_group != self.session.vars['idd'] and self.round_number == 21:
            return True
        else:
            return False


class Questionaire(Page):
    form_model = "player"
    form_fields = ["age", "gender", "income"]

    def is_displayed(self):
        if self.round_number == 21:
            return True
        else:
            return False


class Final_Thank_you(Page):
    def vars_for_template(self):
        acc_profit = self.player.payoff
        acc_dollar = acc_profit.to_real_world_currency(self.session)
        return dict(
            acc_profit=acc_profit,
            acc_dollar=acc_dollar,
            acc_final=acc_dollar + self.session.config['participation_fee']
        )
    def is_displayed(self):
        if self.round_number == 21:
            return True
        else:
            return False

class contribution_table(Page):
    form_model = "player"
    form_fields = ["q"]

    def vars_for_template(self):
        conditional_round = self.round_number - 1

        return dict(
            condi_round = conditional_round

            )

class Results_LastRound(Page):
    def is_displayed(self):
        if self.player.id_in_group == self.session.vars['idd'] and self.round_number == 21:
            return True
        else:
            return False


page_sequence = [ID, consent, Instruction, Quiz, Quiz2_1, Contribute_first_page, contribution_table, ResultsWaitPage, Results,
                  Results_LastRound, Questionaire, Final_Thank_you]
