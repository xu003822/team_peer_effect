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
    tot_other_avg = models.FloatField(label="the group's other members' average contribution")
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
        from decimal import localcontext, Decimal, ROUND_HALF_UP
        with localcontext() as ctx:
            ctx.rounding = ROUND_HALF_UP

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
                self.tot_contri = p.participant.vars['condi_choice'] + self.session.vars['other_average'] * (Constants.num_team - 1)

        self.tot_other_avg = self.session.vars['other_average']

        self.individual_share = Constants.multiplier * self.tot_contri / Constants.num_team
        self.individual_share = self.individual_share.to_integral_value()

        for p in self.get_players():
                if p.participant.vars['audit_or_not'] == 0:
                    p.payoff = Constants.endowment - p.participant.vars['first_round_contri'] + self.individual_share
                # p.payoff = Constants.endowment - p.participant.vars['contri'] + self.individual_share
                else:
                    p.payoff = Constants.endowment - p.participant.vars['condi_choice'] + self.individual_share



    def set_payoff1(self):
        from decimal import localcontext, Decimal, ROUND_HALF_UP
        with localcontext() as ctx:
            ctx.rounding = ROUND_HALF_UP

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

            self.session.vars['other_average'] = self.tot_other_contri / (Constants.num_team - 1)

            self.session.vars['other_average'] = self.session.vars['other_average'].to_integral_value()


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
        #generate an indicator indicating that everyone has reached a decision
        for p in large_group:
            p.participant.vars['conditional_round'] = 0
            p.participant.vars['condi_list'] = []
            if p.participant.vars['agree'] == 0:
               self.session.vars['agreed'] = 0


def quiz1_question(label):
    return models.IntegerField(
        choices=[44, 60, 80, 120],
        widget=widgets.RadioSelect,
        label=label
    )


def quiz2_question(label):
    return models.IntegerField(
        choices=[40, 56, 72, 120],
        widget=widgets.RadioSelect,
        label=label
    )


def quiz3_question(label):
    return models.IntegerField(
        choices=[40, 60, 76, 120],
        widget=widgets.RadioSelect,
        label=label
    )


def quiz4_question(label):
    return models.IntegerField(
        choices=[60, 76, 96, 120],
        widget=widgets.RadioSelect,
        label=label
    )


class Player(BasePlayer):
    id_number = models.IntegerField(label="Please enter your ID number here", min=0, max=300)
    acc_payoff = models.CurrencyField(label="The player's accumulative payoff is ")
    act_payoff = models.CurrencyField(label="The player's accumulative payoff in canadian dollar is")
    actpar_payoff = models.CurrencyField(label="The player's final payoff including the participation fee is")
    contribution = models.IntegerField(label="How many tokens you decide to contribute in this round", min=0, max=20)

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

    def chat_nickname(self):
        # return 'Group {}, Player {}'.format(self.group.id_in_subsession, self.id_in_group)
        return '{}, Player_{}'.format(self.role(), self.id_in_group)

    quiz1_all = quiz1_question(
        "1. Suppose you contribute 20 fish this round and your group mates altogether extract 120 fish. How many fish you will get for this round?")
    quiz2_all = quiz2_question(
        "2. Suppose you extract 40 fish this round and your group mates altogether extract 80 fish. How many fish you will get for this round?")

    quiz3_all = quiz3_question(
        "1. Suppose you extract 60 fish this round and your group mates altogether extract 100 fish. How many fish you will get for this round?")
    quiz4_all = quiz4_question(
        "2. Suppose you extract 80 fish this round and your group mates altogether extract 80 fish. How many fish you will get for this round?")

    def quiz1_all_error_message(self, quiz1_all):
        if quiz1_all != 44:
            self.participant.vars['quiz'] = 0
            return 'Your answer for this quesiton is incorrect. The correct answer is 44. The reason being that since the whole group catches 140 fish, there will be 60 fish left. At' \
                   ' the end of the round, the fish amount doubles to 120. So each player gets an extra 24 fish at the end of the round. So you will in total get 44 fish.' \
                   ' If you are still unclear, please ask the instructor on how to answer this question. Next let\'s try another quiz!'

    def quiz2_all_error_message(self, quiz2_all):
        if quiz2_all != 72:
            self.participant.vars['quiz'] = 0
            return 'Your answer for this question is incorrect. The correct answer is 72. The reason being that since the whole group catches 120 fish, there will be 80 fish left. At' \
                   ' the end of the round, the fish amount doubles to 160. So each player gets an extra 32 fish at the end of the round. So you will in total get 72 fish.' \
                   ' If you are still unclear, please ask the instructor on how to answer this question. Next let\'s try another quiz!'

    def quiz3_all_error_message(self, quiz3_all):
        if quiz3_all != 76:
            return 'Your answer for this quesiton is incorrect. The correct answer is 76. The reason being that since the whole group catches 160 fish, there will be 40 fish left. At' \
                   ' the end of the round, the fish amount doubles to 80. So each player gets an extra 16 fish at the end of the round. So you will in total get 76 fish.' \
                   ' If you are still unclear, please ask the instructor on how to answer this question.'

    def quiz4_all_error_message(self, quiz4_all):
        if quiz4_all != 96:
            return 'Your answer for this question is incorrect. The correct answer is 96. The reason being that since the whole group catches 160 fish, there will be 40 fish left. At' \
                   ' the end of the round, the fish amount doubles to 80. So each player gets an extra 16 fish at the end of the round. So you will in total get 96 fish.' \
                   ' If you are still unclear, please ask the instructor on how to answer this question.'
