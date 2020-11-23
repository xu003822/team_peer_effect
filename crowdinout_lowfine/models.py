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
    name_in_url = 'crowdinout'
    players_per_group = 2
    num_rounds = 6
    multiplier = 2
    fine = 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    tot_extraction = models.IntegerField(label="The group's total catch is ")
    individual_share = models.FloatField(label="At the end of the round, each of you get extra amount fish of")
    audit = models.IntegerField(label="The person who is randomly audit is player number")
    auditplayer_extrac = models.IntegerField(label="The audited individual's catch is")
    def set_payoff(self):
        import random
        players = self.get_players()
        extractions = [p.extraction for p in players]
        self.tot_extraction = sum(extractions)
        self.individual_share = (200 - self.tot_extraction) * Constants.multiplier / Constants.players_per_group


        for p in players:
            if random.randint(1, 20) == 1 and p.extraction > 20 and self.round_number in [3, 4]:
                p.payoff = p.extraction + self.individual_share - Constants.fine * (p.extraction - 20)
            else:
                p.payoff = p.extraction + self.individual_share


class Player(BasePlayer):
      extraction = models.IntegerField(label="how many fish you decide to catch in this round", min=0, max=40)
      age = models.IntegerField(label="What's your age?")
      gender = models.StringField(label="What's your gender?",
                                  choices=["Male","Female","other","Prefer not to say"]
      )
      income = models.FloatField(label="What's your family income?")


