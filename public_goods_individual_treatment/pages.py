from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class consent(Page):
    form_model = 'player'
    form_fields = ['consent']



class Disagree(Page):
    # Display this page only if paricipant disagrees with the terms.
    def is_displayed(self):
        return self.player.consent == 0


class Instruction(Page):
    form_model = 'player'
    form_fields = ['id_number']



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
        if self.round_number <= 4:
            return True
        else:
            return False



class Results(Page):
    def is_displayed(self):
        if self.player.id_in_group != self.session.vars['idd'] and self.round_number == 4:
            return True
        else:
            return False


class Questionaire(Page):
    form_model = "player"
    form_fields = ["age", "gender", "income"]

    def is_displayed(self):
        if self.round_number == 4:
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
        if self.round_number == 4:
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
        if self.player.id_in_group == self.session.vars['idd']  and self.round_number== 4:
            return True
        else:
            return False




page_sequence = [consent, Disagree, Instruction, Contribute_first_page, contribution_table, ResultsWaitPage, Results,
                  Results_LastRound, Questionaire, Final_Thank_you]