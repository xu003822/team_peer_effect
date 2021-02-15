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
    name_in_url = 'crowdinout_social_influence'
    players_per_group = 2
    num_rounds = 9
    multiplier = 2
    fine = 10
    conversion = 0.1
    prac_rounds = 2


class Subsession(BaseSubsession):
      pass
#      def roundnm(self):
#          roundnumber=self.round_number-1
#          return roundnumber
#

class Group(BaseGroup):
    tot_extraction = models.IntegerField(label="The group's total catch is ")
    individual_share = models.FloatField(label="At the end of the round, each of you gets extra amount fish of")
    audit = models.IntegerField(label="The person who is randomly audit is player number")
    auditplayer_extrac = models.IntegerField(label="The audited individual's catch is")
    #audit_id = models.IntegerField(label="The audited player's id is")

    def set_payoff(self):
        import random
        players = self.get_players()
        extractions = [p.extraction for p in players]
        self.tot_extraction = sum(extractions)
        if (200-self.tot_extraction) * Constants.multiplier < 200:
            self.individual_share = (200 - self.tot_extraction) * Constants.multiplier / Constants.players_per_group
        else:
            self.individual_share = 200/Constants.players_per_group


        #the following chooses the person who will be imposed a regulation
        if self.round_number in [Constants.num_rounds - 5, Constants.num_rounds - 4]:
            self.audit = random.randint(1, 4)
            playeraudit = self.get_player_by_id(self.audit)
            self.auditplayer_extrac = playeraudit.extraction
            #self.audit_id =
            #the session.vars store a global variable
            self.session.vars['idd'] = playeraudit.participant.vars['idnumber']

        #the following is saying that only the person who is chosen to impose regulation will be randomly audited and have a fine
        for p in players:
            if random.randint(1, 10) == 1 and p.extraction > 20 and self.round_number in [Constants.num_rounds - 4, Constants.num_rounds - 3] \
                    and p.id_in_group == self.audit:
                p.individual_fine = Constants.fine * (
                            p.extraction - 20)  # determining audited individual's fine and export to the page
                p.payoff = p.extraction + self.individual_share - Constants.fine * (p.extraction - 20)
                p.audit_or_not = 1

            elif random.randint(1, 10) != 1 and p.extraction > 20 and self.round_number in [Constants.num_rounds - 4, Constants.num_rounds - 3] \
                    and p.id_in_group == self.audit:
                p.individual_fine = 0
                p.audit_or_not = 0
                p.payoff = p.extraction + self.individual_share

            else:
                p.individual_fine = 0
                p.audit_or_not = 2 #the subject is not subject to regulation
                p.payoff = p.extraction + self.individual_share

        for p in players:
            if self.round_number > 2:
                p.acc_payoff = p.participant.payoff - p.in_round(1).payoff - p.in_round(
                    2).payoff  # participant.payoff is the historical payoff
                p.act_payoff = p.acc_payoff * Constants.conversion
                p.actpar_payoff = p.act_payoff + self.session.config['participation_fee']


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
        choices = [40, 60, 76, 120],
        widget = widgets.RadioSelect,
        label = label
    )

def quiz4_question(label):
    return models.IntegerField(
        choices = [60, 76, 96, 120],
        widget = widgets.RadioSelect,
        label = label
    )



class Player(BasePlayer):
    id_number = models.IntegerField(label="Please enter your ID number here", min=0, max=40)
    acc_payoff = models.CurrencyField(label="The player's accumulative payoff is ")
    act_payoff = models.CurrencyField(label="The player's accumulative payoff in canadian dollar is")
    actpar_payoff = models.CurrencyField(label="The player's final payoff including the participation fee is")
    extraction = models.IntegerField(label="how many fish you decide to catch in this round", min=0, max=40)
    individual_fine = models.IntegerField(label="The audited indiviudal's fine is ")
    audit_or_not = models.IntegerField(label="The individual is audited or not and whether regulated or not")
    age = models.IntegerField(label="What's your age?")
    gender = models.StringField(label="What's your gender?",
                                choices=["Male", "Female", "other", "Prefer not to say"]
                                )

    income = models.FloatField(label="What's your family income per year?")
    party = models.StringField(label="Are you a member of the Chinese Community Party?",
                               choices=["Yes", "No", "Prefer not to say"]
                               )
    strategy = models.StringField(
        label="Did you change your contribution after the regulation is imposed? If yes, why? If no, why not?",
        )
    strategy_repeal = models.StringField(
        label="Did you change your contribution after the regulation is repealed? If yes, why? If no, why not?",
    )

    consent = models.BooleanField()  # Record participant's consent.
    # Quiz QUESTIONS
    # Question 1

    quiz1_all = quiz1_question(
        "1. Suppose you extract 20 fish this round and your group mates altogether extract 120 fish. How many fish you will get for this round?")
    quiz2_all = quiz2_question(
        "2. Suppose you extract 40 fish this round and your group mates altogether extract 80 fish. How many fish you will get for this round?")

    quiz3_all = quiz3_question(
        "1. Suppose you extract 60 fish this round and your group mates altogether extract 100 fish. How many fish you will get for this round?")
    quiz4_all = quiz4_question(
        "2. Suppose you extract 80 fish this round and your group mates altogether extract 80 fish. How many fish you will get for this round?")

    def quiz1_all_error_message(self, quiz1_all):
        self.participant.vars['quiz'] = 1
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
