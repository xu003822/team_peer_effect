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


        #the following chooses the person who will be imposed a regulation
        if self.round_number in [Constants.num_rounds - 4, Constants.num_rounds - 3]:
            self.audit = random.randint(1, 2)
            playeraudit = self.get_player_by_id(self.audit)
            self.auditplayer_extrac = playeraudit.extraction
            self.audit_id = playeraudit.participant.vars['idnumber']

        #the following is saying that only the person who is chosen to impose regulation will be randomly audited and have a fine
        for p in players:
            if random.randint(1, 20) == 1 and p.extraction > 20 and self.round_number in [Constants.num_rounds - 4, Constants.num_rounds - 3] and p.id_in_group == self.audit:
                p.payoff = p.extraction + self.individual_share - Constants.fine * (p.extraction - 20)
            else:
                p.payoff = p.extraction + self.individual_share

def quiz_question(label):
    return models.IntegerField(
        choices = [44, 60, 80, 120],
        widget = widgets.RadioSelect,
        label = label
    )



class Player(BasePlayer):
      extraction = models.IntegerField(label="how many fish you decide to catch in this round", min=0, max=40)
      age = models.IntegerField(label="What's your age?")
      gender = models.StringField(label="What's your gender?",
                                  choices=["Male","Female","other","Prefer not to say"]
      )
      income = models.FloatField(label="What's your family income per year?")

      consent = models.BooleanField()  # Record participant's consent.
      # Quiz QUESTIONS
      # Question 1
      quiz1_all = quiz_question("1. Suppose you extract 20 fish this round and your group mates altogether extract 120 fish. How many fish you will get for this round?")

      def set_payoff(self):
          self.paid = (self.payoff * Constants.conversion)

      def quiz1_all_error_message(self, quiz1_all):
          if quiz1_all != 44:
             return 'Incorrect. Please ask the instructor on how to answer this question and then resubmit your answer.'

