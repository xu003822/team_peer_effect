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
    name_in_url = 'crowdinout_highfine'
    players_per_group = 4
    multiplier = 2
    fine = 10
    conversion = 0.04
    prac_rounds = 2
    prob_detect = 10
    rounds_interval = 6
    num_rounds = 3 * rounds_interval + 3


class Subsession(BaseSubsession):
    pass


#      def roundnm(self):
#          roundnumber=self.round_number-1
#          return roundnumber
#
# subsessionobj=Subsession(BaseSubsession)

class Group(BaseGroup):
    tot_extraction = models.IntegerField(label="The group's total catch is ")
    individual_share = models.FloatField(label="At the end of the round, each of you gets extra amount fish of")
    audit = models.IntegerField(label="The person who is randomly audit is player number")
    auditplayer_extrac = models.IntegerField(label="The audited individual's catch is")
    audit_id = models.IntegerField(label="The audited player's id is")

    def set_payoff(self):
        import random
        players = self.get_players()
        extractions = [p.extraction for p in players]
        self.tot_extraction = sum(extractions)
        if (200 - self.tot_extraction) * Constants.multiplier < 200:
            self.individual_share = (200 - self.tot_extraction) * Constants.multiplier / Constants.players_per_group
        else:
            self.individual_share = 200 / Constants.players_per_group

        for p in players:
            # 10% chance of getting a fine
            if random.randint(1, Constants.prob_detect) == 1 and p.extraction > (
                    100 / Constants.players_per_group) and self.round_number in range(
                    Constants.num_rounds - 2 * Constants.rounds_interval,
                    Constants.num_rounds - Constants.rounds_interval):
                p.individual_fine = Constants.fine * (p.extraction - (
                            100 / Constants.players_per_group))  # determining audited individual's fine and export to the page
                p.payoff = p.extraction + self.individual_share - Constants.fine * (
                            p.extraction - (100 / Constants.players_per_group))
                p.audit_or_not = 1
            else:
                p.individual_fine = 0
                p.audit_or_not = 0
                p.payoff = p.extraction + self.individual_share

        for p in players:
            if self.round_number > 2:
                p.acc_payoff = p.participant.payoff - p.in_round(1).payoff - p.in_round(
                    2).payoff  # participant.payoff is the historical payoff
                p.participant.vars['acc_payoff'] = p.acc_payoff
                # p.act_payoff = p.acc_payoff * Constants.conversion
                # p.actpar_payoff = p.act_payoff + self.session.config['participation_fee']

            # if self.round_number in range(Constants.num_rounds - 12, Constants.num_rounds - 6):
            # self.audit = random.randint(1, Constants.players_per_group)
            # playeraudit = self.get_player_by_id(self.audit)
            # self.auditplayer_extrac = playeraudit.extraction
            # self.audit_id = playeraudit.participant.vars['idnumber']


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
    extraction = models.IntegerField(label="How many fish you decide to catch in this round", min=0, max=50)
    other_extra = models.IntegerField(
        label="Please also enter your expectation of the average catch of other group members", min=0, max=50)
    individual_fine = models.IntegerField(label="The audited indiviudal's fine is ")
    audit_or_not = models.BooleanField(label="The individual is audited or not")
    age = models.IntegerField(label="What's your age?")
    gender = models.StringField(label="What's your gender?",
                                choices=["Male", "Female", "other", "Prefer not to say"]
                                )

    income = models.FloatField(label="What's your family income per month?")
    party = models.StringField(label="Are you a member of the Chinese Community Party?",
                               choices=["Yes", "No", "Prefer not to say"]
                               )
    strategy = models.StringField(
        label="Did you change your contribution after the regulation was imposed? If yes, why? If no, why not?",
        )
    strategy_repeal = models.StringField(
        label="Did you change your contribution after the regulation was repealed? If yes, why? If no, why not?",
    )

    consent = models.BooleanField()  # Record participant's consent.
    # rand_choice = models.IntegerField(label="The decision that is randomly picked by the experimenter")
    # condi_choice = models.IntegerField(
    #     label="what's the contribution for the decision randomly chosen in the last round")
    # other_choice = models.IntegerField(
    #     label="what's others' average contribution in the last round")
    # Quiz QUESTIONS
    # Question 1
    q1 = models.IntegerField(label="", min=0, max=50)
    q2 = models.IntegerField(label="", min=0, max=50)
    q3 = models.IntegerField(
        label="", min=0, max=50)
    q4 = models.IntegerField(
        label="", min=0, max=50)
    q5 = models.IntegerField(
        label="", min=0, max=50)
    q6 = models.IntegerField(
        label="", min=0, max=50)
    q7 = models.IntegerField(
        label="", min=0, max=50)
    q8 = models.IntegerField(
        label="", min=0, max=50)
    q9 = models.IntegerField(
        label="", min=0, max=50)

    quiz1_all = quiz1_question(
        "1. Suppose you extract 20 fish this round and your group mates altogether extract 120 fish. How many fish you will get for this round?")
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
