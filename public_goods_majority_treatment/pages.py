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

class contribution_conditional(Page):
    form_model = "player"
    form_fields = ["q"]
    def is_displayed(self):
        if self.session.vars['agreed'] == 1 and self.player.participant.vars['conditional_round'] < 21:
            return True
        else:
            return False

    # def vars_for_template(self):
    #     others = self.session.vars['conditional_round']
    #
    #     return dict(
    #         others=others
    #     )

class contribution_conditional_repeat(Page):
    form_model = "player"
    form_fields = ["q"]
    def is_displayed(self):
        if self.player.participant.vars['agree_condi'] == 0:
            return True
        else:
            return False

    # def vars_for_template(self):
    #     others = self.session.vars['conditional_round']
    #
    #     return dict(
    #         others=others
    #     )
# #as long as all player contributes differently, show the same contribution page
class Contribute_first_page_repeat(Page):
    form_model = "player"
    form_fields = ["contribution"]
    def is_displayed(self):
        if self.player.participant.vars['agree'] == 0:
            return True
        else:
            return False

class ResultsWaitConditional(WaitPage):
    after_all_players_arrive = 'set_payoff_conditional'
    title_text = "Waiting Page"
    body_text = "Waiting for others (including other teams) to finish their decisions"

    def is_displayed(self):
        if self.session.vars['agreed'] == 1:
            return True
        else:
            return False


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoff'
    title_text = "Waiting Page"
    body_text = "Waiting for others (including other teams) to finish their decisions"

    def is_displayed(self):
       if self.round_number == 1:
          return True
       else:
          return False

class ResultsWaitPage1(WaitPage):
    after_all_players_arrive = 'set_payoff1'
    title_text = "Waiting Page"
    body_text = "Waiting for others (including other teams) to finish their decisions"

    def is_displayed(self):
        if self.player.participant.vars['agree_condi'] == 2:
            return True
        else:
            return False

class ResultsWaitFinal(WaitPage):
    after_all_players_arrive = 'last_round_payoff'
    title_text = "Waiting Page"
    body_text = "Waiting for others (including other teams) to finish their decisions"

    def is_displayed(self):
        if self.player.participant.vars['conditional_round'] == 21 and self.session.vars['all_finished'] == 1:
            return True
        else:
            return False


class Results_Agree(Page):
    def is_displayed(self):
        if (self.player.participant.vars['agree'] == 1 or self.player.participant.vars['agree_condi'] == 1) \
                and self.player.participant.vars['conditional_round'] < 21:
            return True
        else:
            return False

class Results_Disagree(Page):
    def is_displayed(self):
        if self.player.participant.vars['agree'] == 0 or self.player.participant.vars['agree_condi'] == 0:
            return True
        else:
            return False

class WaitingOther_Condi(Page):
    def is_displayed(self):
        if self.player.participant.vars['agree_condi'] == 1 and self.player.participant.vars['conditional_round'] >= 21:
            return True
        else:
            return False

class Results_LastRound(Page):
    def is_displayed(self):
        if self.player.participant.vars['conditional_round'] >= 21:
           if self.session.vars['all_finished'] == 1 and self.player.participant.vars['audit_or_not'] == 1:
              return True
           else:
              return False

class Results_LastRound_notaudit(Page):
    def is_displayed(self):
        if self.player.participant.vars['conditional_round'] >= 21:
           if self.session.vars['all_finished'] == 1 and self.player.participant.vars['audit_or_not'] != 1:
              return True
           else:
              return False


class Questionaire(Page):
    def is_displayed(self):
        if self.player.participant.vars['conditional_round'] == 21 and self.session.vars['all_finished'] == 1:
            return True
        else:
            return False

    form_model = "player"
    form_fields = ["age", "gender", "income"]

class Final_Thank_you(Page):
    def is_displayed(self):
        if self.player.participant.vars['conditional_round'] == 21 and self.session.vars['all_finished'] == 1:
            return True
        else:
            return False

    def vars_for_template(self):
        acc_profit = self.player.payoff
        acc_dollar = acc_profit.to_real_world_currency(self.session)
        return dict(
            acc_profit=acc_profit,
            acc_dollar=acc_dollar,
            acc_final=acc_dollar + self.session.config['participation_fee']
        )
# class Results_LastRound(Page):
#     def is_displayed(self):
#         if self.player.audit_or_not == 1:
#             return True
#         else:
#             return False
#
page_sequence = [ID, consent, Instruction, Quiz, Quiz2_1, Contribute_first_page, ResultsWaitPage, Results_Disagree, Results_Agree,
                 Contribute_first_page_repeat, ResultsWaitPage1, contribution_conditional,
                 contribution_conditional_repeat, ResultsWaitConditional, WaitingOther_Condi, ResultsWaitFinal, Results_LastRound,
                 Results_LastRound_notaudit,
                 Questionaire, Final_Thank_you]
