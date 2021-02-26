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
        self.participant.vars['quiz'] = 1

        if self.round_number == 1:
           self.participant.vars['idnumber'] = self.player.id_number

    def is_displayed(self):
        if self.round_number == 1:
            return True
        else:
            return False

    def vars_for_template(self):
        max_fish = int(200 / Constants.players_per_group)
        return dict(
            max_fishh=max_fish
        )

class Quiz(Page):
    form_model = 'player'
    form_fields = ['quiz1_all','quiz2_all']

    def is_displayed(self):
        if self.round_number == 1:
            return True
        else:
            return False

    def vars_for_template(self):
        max_fish = int(200/Constants.players_per_group)
        return dict(
            max_fishh = max_fish
            )

class Quiz2_1(Page):
    form_model = 'player'
    form_fields = ['quiz3_all','quiz4_all']

    def is_displayed(self):
        if self.participant.vars['quiz'] == 0 and self.round_number == 1:
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

    def vars_for_template(self):
        max_fish = int(200/Constants.players_per_group)
        return dict(
            max_fishh = max_fish
            )  # it seems you have to put the variables in a dictionary which contains all variables you send to the template

class Practice2(Page):
    form_model = "player"
    form_fields = ["extraction"]

    def is_displayed(self):
        if self.round_number == 2:
            return True
        else:
            return False
    def vars_for_template(self):
        max_fish = int(200/Constants.players_per_group)
        return dict(
            max_fishh = max_fish
            )

class Fine_Instruction(Page):
    def is_displayed(self):
        if self.round_number == (Constants.num_rounds - 2*Constants.rounds_interval):
            return True
        else:
            return False

    def vars_for_template(self):
        quotta = int(100 / Constants.players_per_group)

        return dict(
            quota = quotta
            )

class regulation_audit(Page):
    form_model = "player"
    form_fields = ["extraction"]

    def is_displayed(self):
        #if the player does not get audited and also the round is in the auditing round
        if  self.round_number in range(Constants.num_rounds - 2*Constants.rounds_interval, Constants.num_rounds - Constants.rounds_interval):
            return True
        else:
            return False

    def vars_for_template(self):
        round_numb = self.round_number - 2
        max_fish = int(200 / Constants.players_per_group)

        return dict(
            round_nm=round_numb,
            max_fishh = max_fish
            )


class Revoke_Instruction(Page):

    def is_displayed(self):
        if self.round_number == Constants.num_rounds - Constants.rounds_interval:
           return True
        else:
           return False

class Contribute_first_page(Page):
    form_model = "player"
    form_fields = ["extraction"]

    def is_displayed(self):
        if  self.round_number in [1, 2, Constants.num_rounds] or (self.round_number in
            range(Constants.num_rounds - 2*Constants.rounds_interval, Constants.num_rounds - Constants.rounds_interval)):
            return False
        else:
            return True

    def vars_for_template(self):
        round_numb = self.round_number - 2

        return dict(
            round_nm=round_numb
            )  # it seems you have to put the variables in a dictionary which contains all variables you send to the template

class Results_audited(Page):
    def is_displayed(self):
        #if the player gets audited and also the round is in the auditing round
        if (self.round_number in range(Constants.num_rounds - 2*Constants.rounds_interval, Constants.num_rounds - Constants.rounds_interval)) and self.player.audit_or_not == 1:
            return True
        else:
            return False


class Results_notaudited(Page):
    def is_displayed(self):
        #if the player does not get audited and also the round is in the auditing round
        if (self.round_number in range(Constants.num_rounds - 2*Constants.rounds_interval, Constants.num_rounds - Constants.rounds_interval)) and self.player.audit_or_not == 0:
            return True
        else:
            return False


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoff'
    def is_displayed(self):
        if self.round_number != Constants.num_rounds:
            return True
        else:
            return False

class ResultsPractice(Page):
    def is_displayed(self):
        if self.round_number == 2:
            return True
        else:
            return False

class Results_noreg(Page):
    def is_displayed(self):
        if  self.round_number in range(Constants.num_rounds - 2*Constants.rounds_interval, Constants.num_rounds - Constants.rounds_interval) and self.player.audit_or_not == 2:
            return True
        else:
            return False

class Results(Page):
    def is_displayed(self):
        if  self.round_number == 2 or (self.round_number in range(Constants.num_rounds - 2*Constants.rounds_interval, Constants.num_rounds - Constants.rounds_interval)) \
                or self.round_number == Constants.num_rounds:
            return False
        else:
            return True

#(self.round_number not in [Constants.num_rounds - 3, Constants.num_rounds - 4]) or

class Questionaire(Page):
    form_model = "player"
    form_fields = ["age", "gender", "income", "party"]

    def is_displayed(self):
        if self.round_number == Constants.num_rounds:
            return True
        else:
            return False

class Final_Thank_you(Page):
    def vars_for_template(self):
        acc_profit = self.participant.vars['acc_payoff'] + self.participant.vars['lst_profit']
        acc_dollar = acc_profit.to_real_world_currency(self.session)
        return dict(
            acc_profit=acc_profit,
            acc_dollar=acc_dollar,
            acc_final = acc_dollar + self.session.config['participation_fee']
        )


class contribution_table(Page):
    form_model = "player"
    form_fields = ["q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9"]

    def is_displayed(self):
        if self.round_number == Constants.num_rounds:
            return True
        else:
            return False

    def vars_for_template(self):
        max_fish = int(200 / Constants.players_per_group)
        return dict(
            max_fishh=max_fish
        )


class Results_LastRound(Page):
    def is_displayed(self):
        if self.round_number == Constants.num_rounds:
            return True
        else:
            return False

    def vars_for_template(self):
        import random
        if self.round_number == Constants.num_rounds:
            self.participant.vars['rand_choice'] = random.randint(1, 9)
            if self.participant.vars['rand_choice'] == 1:
                self.participant.vars['condi_choice'] = self.player.q1
                self.participant.vars['other_choice'] = 0
            elif self.participant.vars['rand_choice'] == 2:
                self.participant.vars['condi_choice'] = self.player.q2
                self.participant.vars['other_choice'] = 5
            elif self.participant.vars['rand_choice'] == 3:
                self.participant.vars['condi_choice'] = self.player.q3
                self.participant.vars['other_choice'] = 10
            elif self.participant.vars['rand_choice'] == 4:
                self.participant.vars['condi_choice'] = self.player.q4
                self.participant.vars['other_choice'] = 15
            elif self.participant.vars['rand_choice'] == 5:
                self.participant.vars['condi_choice'] = self.player.q5
                self.participant.vars['other_choice'] = 20
            elif self.participant.vars['rand_choice'] == 6:
                self.participant.vars['condi_choice'] = self.player.q6
                self.participant.vars['other_choice'] = 25
            elif self.participant.vars['rand_choice'] == 7:
                self.participant.vars['condi_choice'] = self.player.q7
                self.participant.vars['other_choice'] = 30
            elif self.participant.vars['rand_choice'] == 8:
                self.participant.vars['condi_choice'] = self.player.q8
                self.participant.vars['other_choice'] = 35
            elif self.participant.vars['rand_choice'] == 9:
                self.participant.vars['condi_choice'] = self.player.q9
                self.participant.vars['other_choice'] = 40

        tot_choice = self.participant.vars['other_choice'] * (Constants.players_per_group-1) + self.participant.vars['condi_choice']

        if (200 - tot_choice) * Constants.multiplier < 200:
            ind_share = (200 - tot_choice) * Constants.multiplier / Constants.players_per_group
        else:
            ind_share = 200 / Constants.players_per_group

        last_profit = self.participant.vars['condi_choice'] + ind_share
        self.participant.vars['lst_profit'] = last_profit
        return dict(
            tot_cho = tot_choice,
            extra_share = ind_share,
            ls_profit = last_profit
            )


page_sequence = [consent, Disagree, Instruction, Quiz, Quiz2_1, PracticeRound, Practice, Practice2, Fine_Instruction,
                 Revoke_Instruction, Contribute_first_page, regulation_audit, ResultsWaitPage, ResultsPractice, Results, Results_audited,
                 Results_notaudited, Results_noreg, contribution_table, Results_LastRound, Questionaire, Final_Thank_you]
