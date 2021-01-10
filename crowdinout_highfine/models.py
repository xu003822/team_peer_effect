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
# subsessionobj=Subsession(BaseSubsession)

class Group(BaseGroup):
    tot_extraction = models.IntegerField(label="The group's total catch is ")
    individual_share = models.FloatField(label="At the end of the round, each of you gets extra amount fish of")
    audit = models.IntegerField(label="The person who is randomly audit is player number")
    auditplayer_extrac = models.IntegerField(label="The audited individual's catch is")
    def set_payoff(self):
        import random
        players = self.get_players()
        extractions = [p.extraction for p in players]
        self.tot_extraction = sum(extractions)
        if (200-self.tot_extraction) * Constants.multiplier < 200:
            self.individual_share = (200 - self.tot_extraction) * Constants.multiplier / Constants.players_per_group
        else:
            self.individual_share = 200/Constants.players_per_group

        for p in players:
            if random.randint(1, 20) == 1 and p.extraction > 20 and self.round_number in [Constants.num_rounds-2,
                                                                                          Constants.num_rounds-1]:
                p.payoff = p.extraction + self.individual_share - Constants.fine * (p.extraction - 20)
            else:
                p.payoff = p.extraction + self.individual_share

        for p in players:
            if self.round_number > 2:
               p.acc_payoff = p.participant.payoff - p.in_round(1).payoff - p.in_round(2).payoff #participant.payoff is the historical payoff
               p.act_payoff = p.acc_payoff * Constants.conversion
               p.actpar_payoff = p.act_payoff + self.session.config['participation_fee']

        #for p in players:
            #p.participant.vars['idnumber'] = p.id_number

def quiz1_question(label):
    return models.IntegerField(
        choices = [44, 60, 80, 120],
        widget = widgets.RadioSelect,
        label = label
    )

def quiz2_question(label):
    return models.IntegerField(
        choices = [40, 56, 72, 120],
        widget = widgets.RadioSelect,
        label = label
    )

class Player(BasePlayer):
      id_number = models.IntegerField(label="Please enter your ID number here", min=0, max=40)
      acc_payoff = models.CurrencyField(label="The player's accumulative payoff is ")
      act_payoff = models.CurrencyField(label="The player's accumulative payoff in canadian dollar is")
      actpar_payoff = models.CurrencyField(label="The player's final payoff including the participation fee is")
      extraction = models.IntegerField(label="how many fish you decide to catch in this round", min=0, max=40)
      age = models.IntegerField(label="What's your age?")
      gender = models.StringField(label="What's your gender?",
                                  choices=["Male","Female","other","Prefer not to say"]
      )

      income = models.FloatField(label="What's your family income per year?")
      party = models.StringField(label="Are you a member of the Chinese Community Party?",
                                  choices=["Yes", "No", "Prefer not to say"]
                                  )
      consent = models.BooleanField()  # Record participant's consent.
      # Quiz QUESTIONS
      # Question 1

      quiz1_all = quiz1_question("1. Suppose you extract 20 fish this round and your group mates altogether extract 120 fish. How many fish you will get for this round?")
      quiz2_all = quiz2_question("2. Suppose you extract 40 fish this round and your group mates altogether extract 80 fish. How many fish you will get for this round?")
      #def set_payoff(self):
          #self.paid = (self.payoff * Constants.conversion)

      def quiz1_all_error_message(self, quiz1_all):
          if quiz1_all != 44:
             return 'Your answer for this quesiton is incorrect. The correct answer is 44. The reason being that since the whole group catches 140 fish, there will be 60 fish left. At' \
                    ' the end of the round, the fish amount doubles to 120. So each player gets an extra 24 fish at the end of the round. So you will in total get 44 fish.' \
                    ' If you are still unclear, please ask the instructor on how to answer this question.'

      def quiz2_all_error_message(self, quiz2_all):
          if quiz2_all != 72:
             return 'Your answer for this question is incorrect. The correct answer is 72. The reason being that since the whole group catches 120 fish, there will be 80 fish left. At' \
                    ' the end of the round, the fish amount doubles to 160. So each player gets an extra 32 fish at the end of the round. So you will in total get 72 fish.' \
                    ' If you are still unclear, please ask the instructor on how to answer this question.'
