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
    name_in_url = 'public_goods_individual'
    players_per_group = 4
    multiplier = 2
    endow = 20
    num_rounds=5
    endowment = 20

class Subsession(BaseSubsession):
      pass


class Group(BaseGroup):
    tot_contri = models.IntegerField(label="The group's total contribution is ")
    individual_share = models.FloatField(label="At the end of the round, each of you gets extra amount fish of")
    other_extrac = models.IntegerField(label="the group's other members' total contribution")
    tot_other_avg = models.FloatField(label="the group's other members' average contribution")
    tot_other_contri = models.FloatField(label="the group's other members' average contribution")
    audit = models.IntegerField(label="the group's other members' total contribution")

    def set_payoff(self):
        import random
        from decimal import localcontext, Decimal, ROUND_HALF_UP
        with localcontext() as ctx:
             ctx.rounding = ROUND_HALF_UP

        players = self.get_players()

        if self.round_number == 1:
           self.audit = random.randint(1, Constants.players_per_group)
           self.session.vars['idd'] = self.audit

        if self.round_number == 1:
            for p in players:
                p.participant.vars['condi_list'] = []

        for p in players:
            p.participant.vars['condi_list'].append(p.q)

        if self.round_number == 1:
            for p in players:
                p.participant.vars['contri'] = p.contribution

        #initialize other play's total contribution
        if self.round_number == 1:
           self.tot_other_contri = 0
           for p in players:
               if p.id_in_group != self.session.vars['idd']:
                  self.tot_other_contri = p.contribution + self.tot_other_contri
           self.session.vars['avg_contri'] = self.tot_other_contri / (Constants.players_per_group - 1)
           self.session.vars['avg_contri'] = self.session.vars['avg_contri'].to_integral_value()
           self.session.vars['tot_other_contri'] = self.tot_other_contri

        self.session.vars['condi_choice'] = 0

        if self.round_number == 4:
            for p in players:
                if p.id_in_group == self.session.vars['idd']:
                    for i in range(0,4):
                        if self.session.vars['avg_contri'] == i:
                            self.session.vars['condi_choice'] = p.participant.vars['condi_list'][i]

        self.individual_share = Constants.multiplier * (self.session.vars['tot_other_contri'] + self.session.vars['condi_choice'])/ Constants.players_per_group
        self.individual_share = self.individual_share.to_integral_value()

        for p in players:
            if p.id_in_group != self.session.vars['idd']:
                p.payoff = Constants.endow - p.participant.vars['contri'] + self.individual_share

            if p.id_in_group == self.session.vars['idd']:
                p.payoff = Constants.endow - self.session.vars['condi_choice'] + self.individual_share


        self.tot_contri = self.session.vars['tot_other_contri']+self.session.vars['condi_choice']


def quiz1_question(label):
    return models.IntegerField(
        choices = [25, 30, 35, 40],
        widget = widgets.RadioSelect,
        label = label
    )

def quiz2_question(label):
    return models.IntegerField(
        choices = [10, 22.5, 37.5, 40],
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
      act_payoff = models.CurrencyField(label="The player's accumulative payoff in canadian dollar is")
      actpar_payoff = models.CurrencyField(label="The player's final payoff including the participation fee is")
      contribution = models.IntegerField(label="How many tokens you decide to contribute in this round", min=0, max=20)
      other_contri = models.IntegerField(label="Please also enter your expectation of the average catch of other group members", min=0, max=20)
      audit_or_not = models.BooleanField(label="The individual is audited or not")
      age = models.IntegerField(label="What's your age?")
      gender = models.StringField(label="What's your gender?",
                                  choices=["Male","Female","other","Prefer not to say"]
      )

      income = models.FloatField(label="What's your family income per month?")

      consent = models.BooleanField()  # Record participant's consent.

      q = models.IntegerField(label="", min=0, max=20)

      quiz1_all = quiz1_question("1. If in the first round you decide to contribute 5 tokens and other group members contribute 10, 15, 20 respectively. "
                                 "Imagine that the computer program later randomly selects the player who contributes 20 as the fourth player, for whom the "
                                 "payoff-relevant decision is from "
                                 "the second round. And this player decides to contribute 10 when the average contribution of other players in the"
                                 " first round is 10. What's your final payoff?")

      quiz2_all = quiz2_question("2. If in the first round you decide to contribute 20 tokens and other group members contribute 0, 10, 5 respectively. "
                                 "Imagine that the computer program later randomly selects you as the fourth player, for whom the payoff-relevant decision "
                                 "is from the second round. In the second round, you decide to contribute 10 when the average contribution in the first "
                                 "round is 5. What's your final payoff?")

      quiz3_all = quiz3_question(
          "3. If in the first round you decide to contribute 10 tokens and other group members contribute 5, 15, 20 respectively."
            " Imagine that the experimenter later selects the player who contributes 20, for whom the payoff-relevant decision is his/her "
           "second round decision. And this player decides to contribute 6 when the average contribution of other players in the first round is 10. "
            "What's your final payoff?")

      quiz4_all = quiz4_question(
          "4. If in the first round you decide to contribute 15 tokens and other group members contribute 5, 10, 20 respectively."
            " Imagine that the experimenter later selects the your second round decision as the payoff-relevant decision. And in the second"
                                 " round, you decide to contribute 10 when the average contribution in the first round is 10."
                                 " What's your final payoff?")

      def quiz1_all_error_message(self, quiz1_all):
          if quiz1_all != 35:
             self.participant.vars['quiz'] = 0
             return 'Your answer for this question is {correct, incorrect} (depends on the answer). The correct answer is 35. This is because the fourth player' \
                    ' decides to contribute 20 in the first round and to contribute 10 in the second round if other players’ average contribution is 10 [(5+10+15)/3] ' \
                    'in the first round. The group’s ' \
                    'total contribution to the POOL is thus 5 + 10 +15 + 10 = 40. Each player’s earning from the POOL is thus 40*2/4 = 20. Your final payoff is ' \
                    '20 - 5 + 20 = 35.'

      def quiz2_all_error_message(self, quiz2_all):
          if quiz2_all != 20:
             self.participant.vars['quiz'] = 0
             return 'Your answer for this question is {correct, incorrect} (depends on the answer).  The correct answer is 22.5. ' \
                    'This is because your second round decision is the payoff-relevant decision. In this round you decide to contribute ' \
                    '10 when other players on average contributed 5 in the first round. The group total contribution is thus 0 + 10 + 5 +10 = 25.' \
                    ' Each individual earnings from the POOL is thus 25*2/4 = 12.5.  Your final payoff is 20 - 10 + 12.5 = 22.5.'

      def quiz3_all_error_message(self, quiz3_all):
          if quiz3_all != 28:
             return 'Your answer for this quesiton is incorrect. The correct answer is 28.' \
                    ' This is because the player who contributes 20 in the first round' \
                    ' contributes 6 in the second round when other players on average contribute 10 in the first round. ' \
                    'The group total contribution is thus 6 + 5 + 10 +15 = 36. ' \
                    'Each individual earnings from the project is thus 36*2/4 = 18.'\
                    ' Your final payoff is 20 - 10 + 18 = 28.' \

      def quiz4_all_error_message(self, quiz4_all):
          if quiz4_all != 25:
              return 'Your answer for this question is incorrect. The correct answer is 25. This is because your second round decision is the payoff-relevant decision.' \
                     ' And you decide to contribute 10 when other players on average contribute 10 in the first round. The group total contribution is thus 10 + 5 + 10 +15 = 40. ' \
                     'Each individual earnings from the project is thus 40*2/4 = 20.' \
                     'Your final payoff is 20 - 15 + 20 = 25.'