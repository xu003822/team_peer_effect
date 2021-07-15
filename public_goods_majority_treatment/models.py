from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'public_goods_majority'
    players_per_group = 12
    num_team = 4
    multiplier = 2
    endow = 20
    num_rounds = 100 #this allows repeated play
    endowment = 20
    subnum = 3 #the number of people in a team


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    tot_contri = models.IntegerField(label="The group's total contribution is ")
    individual_share = models.FloatField(label="At the end of the round, each of you gets extra amount fish of")
    other_extrac = models.IntegerField(label="the group's other members' total contribution")
    tot_other_avg = models.IntegerField(label="the group's other members' average contribution")
    tot_other_contri = models.FloatField(label="the group's other members' average contribution")


    def set_payoff_conditional(self):

        large_group = self.get_players()
        # A contains 4 subgroup
        A = []
        A.append([p for p in large_group if p.id_in_group in range(1, 4)])
        A.append([p for p in large_group if p.id_in_group in range(4, 7)])
        A.append([p for p in large_group if p.id_in_group in range(7, 10)])
        A.append([p for p in large_group if p.id_in_group in range(10, 13)])

        j = 0

        self.session.vars['all_finished'] = 1

        for i in range(0, 4):
                if A[i][j].participant.vars['conditional_round'] < 4:
                    if A[i][j].q != A[i][j + 1].q and A[i][j + 1].q != A[i][j + 2].q and \
                            A[i][j].q != A[i][j + 2].q:
                        for p in A[i]:
                            p.participant.vars['agree_condi'] = 0
                            p.participant.vars['agree'] = 2  # so that we don't go back to the first round's result page
                            p.participant.vars['contri'] = 0  # initialize value, could be any value
                    elif A[i][j].q == A[i][j + 1].q and A[i][j + 1].q != A[i][j + 2].q:
                        A[i][j + 2].q = A[i][j + 1].q
                        for p in A[i]:
                            p.participant.vars['contri'] = A[i][j + 1].q
                            p.participant.vars['agree_condi'] = 1
                    elif A[i][j].q != A[i][j + 1].q and A[i][j + 1].q == A[i][j + 2].q:
                        A[i][j].q = A[i][j + 1].q
                        for p in A[i]:
                            p.participant.vars['contri'] = A[i][j + 1].q
                            p.participant.vars['agree_condi'] = 1
                    else:
                        for p in A[i]:
                            p.participant.vars['contri'] = A[i][1].q
                            p.participant.vars['agree_condi'] = 1

                    for p in A[i]:
                        if p.participant.vars['agree_condi'] == 1:
                            # ready for next round in the conditional contribution
                            p.participant.vars['conditional_round'] = p.participant.vars['conditional_round'] + 1
                            p.participant.vars['condi_list'].append(p.participant.vars['contri'])

                    # generate an indicator indicating that everyone has reached a decision
        for i in range(0,4):
                # for p in A[i]:
                #     if p.participant.vars['agree_condi'] == 0:
                #         self.session.vars['agreed_final'] = 0
                for p in A[i]:
                        # having an indicator indicating that all teams finish all the conditional contribution decision
                    if p.participant.vars['conditional_round'] < 4:
                        self.session.vars['all_finished'] = 0

    def last_round_payoff(self):

        large_group = self.get_players()
        for p in large_group:
            if p.participant.vars['audit_or_not'] == 1:
                if self.session.vars['other_average'] == 0:
                    p.participant.vars['condi_choice'] = p.participant.vars['condi_list'][0]
                elif self.session.vars['other_average'] == 1:
                    p.participant.vars['condi_choice'] = p.participant.vars['condi_list'][1]
                elif self.session.vars['other_average'] == 2:
                    p.participant.vars['condi_choice'] = p.participant.vars['condi_list'][2]
                elif self.session.vars['other_average'] == 3:
                    p.participant.vars['condi_choice'] = p.participant.vars['condi_list'][3]

                # elif self.session.vars['other_average'] == 4:
                #     p.participant.vars['condi_choice'] = p.participant.vars['condi_list'][4]
                #
                # elif self.session.vars['other_average'] == 5:
                #     p.participant.vars['condi_choice'] = p.participant.vars['condi_list'][5]
                #
                # elif self.session.vars['other_average'] == 6:
                #     p.participant.vars['condi_choice'] = p.participant.vars['condi_list'][6]
                #
                # elif self.session.vars['other_average'] == 7:
                #     p.participant.vars['condi_choice'] = p.participant.vars['condi_list'][7]
                #
                # elif self.session.vars['other_average'] == 8:
                #     p.participant.vars['condi_choice'] = p.participant.vars['condi_list'][8]
                #
                # elif self.session.vars['other_average'] == 9:
                #     p.participant.vars['condi_choice'] = p.participant.vars['condi_list'][9]
                #
                # elif self.session.vars['other_average'] == 10:
                #     p.participant.vars['condi_choice'] = p.participant.vars['condi_list'][10]
                #
                # elif self.session.vars['other_average'] == 11:
                #     p.participant.vars['condi_choice'] = p.participant.vars['condi_list'][11]
                #
                # elif self.session.vars['other_average'] == 12:
                #     p.participant.vars['condi_choice'] = p.participant.vars['condi_list'][12]
                #
                # elif self.session.vars['other_average'] == 13:
                #     p.participant.vars['condi_choice'] = p.participant.vars['condi_list'][13]
                #
                # elif self.session.vars['other_average'] == 14:
                #     p.participant.vars['condi_choice'] = p.participant.vars['condi_list'][14]
                #
                # elif self.session.vars['other_average'] == 15:
                #     p.participant.vars['condi_choice'] = p.participant.vars['condi_list'][15]
                #
                # elif self.session.vars['other_average'] == 16:
                #     p.participant.vars['condi_choice'] = p.participant.vars['condi_list'][16]
                #
                # elif self.session.vars['other_average'] == 17:
                #     p.participant.vars['condi_choice'] = p.participant.vars['condi_list'][17]
                #
                # elif self.session.vars['other_average'] == 18:
                #     p.participant.vars['condi_choice'] = p.participant.vars['condi_list'][18]
                #
                # elif self.session.vars['other_average'] == 19:
                #     p.participant.vars['condi_choice'] = p.participant.vars['condi_list'][19]
                #
                # elif self.session.vars['other_average'] == 20:
                #     p.participant.vars['condi_choice'] = p.participant.vars['condi_list'][20]

        for p in large_group:
            if p.participant.vars['audit_or_not'] == 1:
                self.tot_contri = p.participant.vars['condi_choice'] + self.tot_other_contri


        self.tot_other_avg = self.session.vars['other_average']

        if Constants.multiplier * self.tot_contri / Constants.num_team - int(Constants.multiplier * self.tot_contri / Constants.num_team) == 0.5:
            self.individual_share = int(Constants.multiplier * self.tot_contri / Constants.num_team) + 1
        else:
            self.individual_share = round(Constants.multiplier * self.tot_contri / Constants.num_team)

        for p in self.get_players():
                if p.participant.vars['audit_or_not'] == 0:
                    p.payoff = Constants.endowment - p.participant.vars['first_round_contri'] + self.individual_share
                # p.payoff = Constants.endowment - p.participant.vars['contri'] + self.individual_share
                else:
                    p.payoff = Constants.endowment - p.participant.vars['condi_choice'] + self.individual_share

                p.acc_payoff = p.payoff.to_real_world_currency(self.session) + self.session.config['participation_fee']



    def set_payoff1(self):

        large_group = self.get_players()
        # A contains 4 subgroup
        A = []
        A.append([p for p in large_group if p.id_in_group in range(1, 4)])
        A.append([p for p in large_group if p.id_in_group in range(4, 7)])
        A.append([p for p in large_group if p.id_in_group in range(7, 10)])
        A.append([p for p in large_group if p.id_in_group in range(10, 13)])

        j = 0

#it does not go through this
        for i in range(0, 4):
              for p in A[i]:
                  if p.participant.vars['agree'] == 0:
                      #using backslash to split the lines. This is so important
                      #note the bracket cannot be in two different lines
                      if A[i][j].contribution != A[i][j + 1].contribution and A[i][j + 1].contribution != A[i][j+2].contribution and A[i][j].contribution != A[i][j + 2].contribution:
                                p.participant.vars['agree'] = 0
                                p.participant.vars['contri'] = 1  # initialize value, could be any value

                      elif A[i][j].contribution == A[i][j + 1].contribution and A[i][j + 1].contribution != A[i][j + 2].contribution:
                                 A[i][j + 2].contribution = A[i][j + 1].contribution
                                 p.participant.vars['contri'] = A[i][j + 1].contribution
                                 p.participant.vars['agree'] = 1

                      elif A[i][j].contribution != A[i][j + 1].contribution and A[i][j + 1].contribution == A[i][j + 2].contribution:
                                 A[i][j].contribution = A[i][j + 1].contribution
                                 p.participant.vars['contri'] = A[i][j + 1].contribution
                                 p.participant.vars['agree'] = 1

                      else:
                              p.participant.vars['contri'] = A[i][1].contribution
                              p.participant.vars['agree'] = 1

        self.session.vars['agreed'] = 1
        # generate an indicator indicating that everyone has reached a decision
        for p in large_group:
            if p.participant.vars['agree'] == 0:
               self.session.vars['agreed'] = 0

            # initialize other play's total contribution
        self.tot_other_contri = 0

        # the following code deal with connection between the unconditional contribution and conditional contribution

        import random
        # the session.vars store the id number of the team who is selected
        self.session.vars['team_id'] = random.randint(1, Constants.num_team)

        if self.session.vars['agreed'] == 1:

            for i in range(0, 4):
                if i == self.session.vars['team_id']:
                    for p in A[i]:
                        p.participant.vars['audit_or_not'] = 1
                else:
                    for p in A[i]:
                        p.participant.vars['audit_or_not'] = 0

            for i in range(0, 4):
                for p in A[i]:
                    p.participant.vars['first_round_contri'] = p.participant.vars['contri'] #record the first round every player's contribution
                    if p.participant.vars['audit_or_not'] == 0:
                        self.tot_other_contri = p.participant.vars['contri'] / Constants.subnum + self.tot_other_contri

            self.session.vars['other_average'] = round(self.tot_other_contri / (Constants.num_team - 1))



    def set_payoff(self):
        import random
        #assign people to four different teams(subgroups)

        large_group = self.get_players()
        # A contains 4 subgroup
        A = []
        A.append([p for p in large_group if p.id_in_group in range(1, 4)])
        A.append([p for p in large_group if p.id_in_group in range(4, 7)])
        A.append([p for p in large_group if p.id_in_group in range(7, 10)])
        A.append([p for p in large_group if p.id_in_group in range(10, 13)])

        j = 0
        for p in large_group:
            p.participant.vars['agree_condi'] = 2  #just give this an initial value

        for i in range(0,4):
            if A[i][j].contribution != A[i][j+1].contribution and A[i][j+1].contribution != A[i][j+2].contribution and A[i][j].contribution != A[i][j+2].contribution:
                   for p in A[i]:
                       p.equal = 0
                       p.participant.vars['agree'] = 0
                       p.participant.vars['contri'] = 0 #initialize value, could be any value
                       #make each individuals' contribution in a subgroup equal to the majority contribution (and thus the subgroup contribution)
            elif A[i][j].contribution == A[i][j+1].contribution and A[i][j+1].contribution != A[i][j+2].contribution:
                    A[i][j + 2].contribution = A[i][j+1].contribution
                    for p in A[i]:
                        p.equal = 1
                        p.participant.vars['contri'] = A[i][j+1].contribution
                        p.participant.vars['agree'] = 1
            elif A[i][j].contribution != A[i][j+1].contribution and A[i][j+1].contribution == A[i][j+2].contribution:
                    A[i][j].contribution = A[i][j + 1].contribution
                    for p in A[i]:
                        p.equal = 1
                        p.participant.vars['contri'] = A[i][j + 1].contribution
                        p.participant.vars['agree'] = 1
            else:
                 for p in A[i]:
                     p.equal = 1
                     p.participant.vars['contri'] = A[i][1].contribution
                     p.participant.vars['agree'] = 1

        self.session.vars['agreed'] = 1
        self.session.vars['all_finished'] = 0

        #generate an indicator indicating that everyone has reached a decision
        for p in large_group:
            p.participant.vars['conditional_round'] = 0
            p.participant.vars['condi_list'] = []
            if p.participant.vars['agree'] == 0:
               self.session.vars['agreed'] = 0


def quiz1_question(label):
    return models.IntegerField(
        choices = [25, 30, 35, 40],
        widget = widgets.RadioSelect,
        label = label
    )

def quiz2_question(label):
    return models.IntegerField(
        choices = [10, 21, 36, 40],
        widget = widgets.RadioSelect,
        label = label
    )

def quiz3_question(label):
    return models.IntegerField(
        choices = [20, 28, 34, 40],
        widget = widgets.RadioSelect,
        label = label
    )

def quiz4_question(label):
    return models.IntegerField(
        choices = [20, 25, 30, 35],
        widget = widgets.RadioSelect,
        label = label
    )

class Player(BasePlayer):
    id_number = models.IntegerField(label="Please enter your ID number here", min=0, max=300)
    acc_payoff = models.CurrencyField(label="The player's accumulative payoff is ")
    contribution = models.IntegerField(label="How many tokens do you want your team to contribute in this round", min=0, max=20)

    other_contri = models.IntegerField(
        label="Please also enter your expectation of the average catch of other group members", min=0, max=20)
    equal = models.IntegerField(label="The individual is audited or not")
    age = models.IntegerField(label="What's your age?")
    gender = models.StringField(label="What's your gender?",
                                choices=["Male", "Female", "other", "Prefer not to say"]
                                )

    income = models.FloatField(label="What's your family income per month?")

    consent = models.BooleanField()  # Record participant's consent.
    q = models.IntegerField(label="", min=0, max=20)


    def role(self):
        if self.id_in_group >= 1 and self.id_in_group <= 3:
            return 'Team_1'
        elif self.id_in_group >= 4 and self.id_in_group <= 6:
            return 'Team_2'
        elif self.id_in_group >= 7 and self.id_in_group <= 9:
            return 'Team_3'
        else:
            return 'Team_4'

    def team_subid(self):
        for i in range(1, 12, 3):
            if self.id_in_group == i:
                return '1'
            if self.id_in_group == i + 1:
                return '2'
            if self.id_in_group == i + 2:
                return '3'

    def chat_nickname(self):
        # return 'Group {}, Player {}'.format(self.group.id_in_subsession, self.id_in_group)
        return '{}, Player_{}'.format(self.role(), self.team_subid())

    quiz1_all = quiz1_question(
        "1. If in the first round your team decides to contribute 5 tokens and other three teams contribute 10, 15, 20 respectively. "
        "Imagine that the computer program later randomly selects the team who contributes 20 as the fourth team, for which the "
        "payoff-relevant decision is from "
        "the second round. And this team decides to contribute 10 when the average contribution of other teams in the"
        " first round is 10. What's your final payoff?")

    quiz2_all = quiz2_question(
        "2. If in the first round your team decides to contribute 20 tokens and other three teams contribute 0, 10, 5 respectively. "
        "Imagine that the computer program later randomly selects your team as the fourth team, for which the payoff-relevant decision "
        "is from the second round. In the second round, your team decides to contribute 10 when the average contribution in the first "
        "round is 5. What's your final payoff?")

    quiz3_all = quiz3_question(
        "3. If in the first round your team decides to contribute 10 tokens and other teams contribute 5, 15, 20 respectively."
        " Imagine that the computer program later randomly selects the team who contributes 20 as the fourth team, for which the payoff-relevant decision is from the "
        "second round. And this team decides to contribute 6 when the average contribution of other teams in the first round is 10. "
        "What's your final payoff?")

    quiz4_all = quiz4_question(
        "4. If in the first round your team decides to contribute 15 tokens and other teams contribute 5, 10, 15 respectively."
        " Imagine that the computer program later randomly selects your team as the fourth team, for which the payoff-relevant decision is from"
        "the second round. In the second"
        " round, your team decides to contribute 10 when the average contribution in the first round is 10."
        " What's your final payoff?")

    def quiz1_all_error_message(self, quiz1_all):
        if quiz1_all != 35:
            self.participant.vars['quiz'] = 0
            return 'Your answer for this question is incorrect. The correct answer is 35. This is because the fourth team' \
                   ' decides to contribute 20 in the first round and to contribute 10 in the second round if other teams’ average contribution is 10 [(5+10+15)/3] ' \
                   'in the first round. The ' \
                   'total contribution to the POOL is thus 5 + 10 +15 + 10 = 40. Each team’s earning from the POOL is thus 40*2/4 = 20. Your team’s final payoff is ' \
                   '20 - 5 + 20 = 35. So your final payoff is 35.'

    def quiz2_all_error_message(self, quiz2_all):
        if quiz2_all != 21:
            self.participant.vars['quiz'] = 0
            return 'Your answer for this question is incorrect.  The correct answer is 21. ' \
                   'This is because your second round decision is the payoff-relevant decision. In this round your team decide to contribute ' \
                   '13 when other teams on average contributed 5 in the first round. The total contribution is thus 0 + 13 + 5 +10 = 28.' \
                   ' Each team’s payoff from the POOL is thus 28*2/4 = 14.  Your team’s final payoff is 20 - 13 + 14 = 21. So your final payoff is 21.'

    def quiz3_all_error_message(self, quiz3_all):
        if quiz3_all != 28:
            return 'Your answer for this quesiton is incorrect. The correct answer is 28.' \
                   ' This is because the team who contributes 20 in the first round' \
                   ' contributes 6 in the second round when other teams on average contribute 10 in the first round. ' \
                   'The total contribution is thus 6 + 5 + 10 +15 = 36. ' \
                   'Each team’s payoff from the POOL is thus 36*2/4 = 18.' \
                   ' Your team’s final payoff is 20 - 10 + 18 = 28. So your final payoff is 28.' \

    def quiz4_all_error_message(self, quiz4_all):
        if quiz4_all != 30:
            return 'Your answer for this question is incorrect. The correct answer is 30. This is because your second ' \
                   'round decision is the payoff-relevant decision.' \
                   ' And your team decides to contribute 10 when other teams on average contribute 10 in the first round. The total contribution ' \
                   'is thus 10 + 5 + 10 +15 = 40. ' \
                   'Each team’s payoff from the POOL is thus 40*2/4 = 20.' \
                   'Your team’s final payoff is 20 - 10 + 20 = 30. So your final payoff is 30.'
