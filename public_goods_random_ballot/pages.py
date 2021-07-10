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

    def is_displayed(self):
       if self.round_number == 1:
          return True
       else:
          return False


# class Quiz(Page):
#     form_model = 'player'
#     form_fields = ['quiz1_all','quiz2_all']
#
#
# class Quiz2_1(Page):
#     form_model = 'player'
#     form_fields = ['quiz3_all','quiz4_all']

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
        if self.session.vars['agreed'] == 1:
            return True
        else:
            return False


class ResultsWaitConditional(WaitPage):
    after_all_players_arrive = 'set_payoff_conditional'

    def is_displayed(self):
        if self.session.vars['agreed'] == 1:
            return True
        else:
            return False


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoff'

    def is_displayed(self):
       if self.round_number == 1:
          return True
       else:
          return False


class ResultsWaitFinal(WaitPage):
    after_all_players_arrive = 'last_round_payoff'

    def is_displayed(self):
        if self.player.participant.vars['conditional_round'] == 4:
            return True
        else:
            return False


class Results_FirstRound(Page):
    def is_displayed(self):
        if self.session.vars['agreed'] == 1:
            return True
        else:
            return False



class Results_LastRound(Page):
    def is_displayed(self):
        if self.player.participant.vars['conditional_round'] == 4 and self.player.participant.vars['audit_or_not']==1:
            return True
        else:
            return False

class Results_LastRound_notaudit(Page):
    def is_displayed(self):
        if self.player.participant.vars['conditional_round'] == 4 and self.player.participant.vars['audit_or_not']!=1:
            return True
        else:
            return False


class Questionaire(Page):
    def is_displayed(self):
        if self.player.participant.vars['conditional_round'] == 4:
            return True
        else:
            return False

    form_model = "player"
    form_fields = ["age", "gender", "income"]


class Final_Thank_you(Page):
    def is_displayed(self):
        if self.player.participant.vars['conditional_round'] == 4:
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
#
page_sequence = [Contribute_first_page, ResultsWaitPage, Results_FirstRound,
                contribution_conditional, ResultsWaitConditional, ResultsWaitFinal, Results_LastRound,
                 Results_LastRound_notaudit,
                Questionaire, Final_Thank_you]
