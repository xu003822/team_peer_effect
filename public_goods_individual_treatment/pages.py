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

class Simulation(Page):
    form_model = 'player'
    form_fields = ['contribution1','contribution2','contribution3','contribution4']

    def is_displayed(self):
        if self.round_number == 1:
            return True
        else:
            return False

class Simulation_result(Page):
    form_model = 'player'

    def is_displayed(self):
        if self.round_number == 1:
            return True
        else:
            return False

    def vars_for_template(self):
        result_sim1 = 20 - self.player.contribution1 + 0.5 * (self.player.contribution1 +
                                                             self.player.contribution2 + self.player.contribution3 + self.player.contribution4)
        result_sim2 = 20 - self.player.contribution2 + 0.5 * (self.player.contribution1 +
                                                              self.player.contribution2 + self.player.contribution3 + self.player.contribution4)
        result_sim3 = 20 - self.player.contribution3 + 0.5 * (self.player.contribution1 +
                                                              self.player.contribution2 + self.player.contribution3 + self.player.contribution4)
        result_sim4 = 20 - self.player.contribution4 + 0.5 * (self.player.contribution1 +
                                                              self.player.contribution2 + self.player.contribution3 + self.player.contribution4)

        result_sum = self.player.contribution1 + self.player.contribution2 + self.player.contribution3 + self.player.contribution4

        result_return = 0.5 * (self.player.contribution1 + self.player.contribution2 + self.player.contribution3 + self.player.contribution4)

        return dict(
            result_sim1=result_sim1,
        result_sim2 = result_sim2,
        result_sim3 = result_sim3,
        result_sim4 = result_sim4,
            result_return = result_return,
            result_sum = result_sum
        )

class QuizSolution(Page):
    form_model = 'player'
    form_fields = ['quiz1_all','quiz2_all']

    def is_displayed(self):
        if self.round_number == 1:
            return True
        else:
            return False

class QuizSolution2(Page):
    form_model = 'player'
    form_fields = ['quiz3_all','quiz4_all']

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

class QuizWaitPage(WaitPage):
    title_text = "Waiting Page"
    body_text = "Waiting for other participants to finish the quizzes"
    def is_displayed(self):
        if self.round_number == 1:
            # before it is self.round_number <= 4:
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


page_sequence = [ID, consent, Instruction, Simulation, Simulation_result, Quiz, QuizSolution, Quiz2_1, QuizSolution2
                 QuizWaitPage, Contribute_first_page, contribution_table, ResultsWaitPage, Results,
                  Results_LastRound, Questionaire, Final_Thank_you]
