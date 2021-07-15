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
    num_rounds=21
    endowment = 20
    ex_rate = 0.1 # exchange rate
    showup = 5


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
           self.session.vars['avg_contri'] = round(self.tot_other_contri / (Constants.players_per_group - 1))
           self.session.vars['tot_other_contri'] = self.tot_other_contri

        self.session.vars['condi_choice'] = 0

        if self.round_number == 21:
            for p in players:
                if p.id_in_group == self.session.vars['idd']:
                    for i in range(0,21):
                        if self.session.vars['avg_contri'] == i:
                            self.session.vars['condi_choice'] = p.participant.vars['condi_list'][i]

        if (Constants.multiplier * (self.session.vars['tot_other_contri'] +
                                                              self.session.vars['condi_choice'])/ Constants.players_per_group) - int(Constants.multiplier * (self.session.vars['tot_other_contri'] +
                                                              self.session.vars['condi_choice'])/ Constants.players_per_group) == 0.5:
            self.individual_share = int(Constants.multiplier * (self.session.vars['tot_other_contri'] +
                                                              self.session.vars['condi_choice'])/ Constants.players_per_group) + 1
        else:
            self.individual_share = round(Constants.multiplier * (self.session.vars['tot_other_contri'] +
                                                              self.session.vars['condi_choice'])/ Constants.players_per_group)


        for p in players:
            if p.id_in_group != self.session.vars['idd']:
                p.payoff = Constants.endow - p.participant.vars['contri'] + self.individual_share

            if p.id_in_group == self.session.vars['idd']:
                p.payoff = Constants.endow - self.session.vars['condi_choice'] + self.individual_share

            p.acc_payoff = p.payoff*Constants.ex_rate + Constants.showup

        self.tot_contri = self.session.vars['tot_other_contri']+self.session.vars['condi_choice']


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
        choices = [20, 31, 34, 40],
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
      contribution = models.IntegerField(label="How many tokens you decide to contribute in this round", min=0, max=20)
      other_contri = models.IntegerField(label="Please also enter your expectation of the average catch of other group members", min=0, max=20)
      audit_or_not = models.BooleanField(label="The individual is audited or not")
      age = models.IntegerField(label="What's your age?")
      gender = models.StringField(label="What's your gender?",
                                  choices=["Male","Female","other","Prefer not to say"]
      )

      income = models.FloatField(label="What's your family income per month?")

      risk = models.IntegerField(label="On  a scale from 1 to 10, how willing or unwilling are you to take "
                                       "risks (1 – completely unwilling to take risks, 10 – very willing to take risks)? ___")
      punish = models.IntegerField(label="How willing are you to punish someone who treats you unfairly, even if there may be "
                                         "costs to yourself to punish them (1 – completely unwilling to do so, 10 – very willing to do so)? ___")
      punish2 = models.IntegerField(label="How willing are you to punish someone who treats other people unfairly, even if "
                                          "there may be costs to yourself to punish them (1 – completely unwilling to do so, 10 – very willing to do so)? ___")
      favor = models.IntegerField(label="How well does the following statement describe you as a person: “When someone does me a favor, "
                                        "I am willing to return it” (1 – does not describe me at all, 10 – describes me perfectly)? ___")

      consent = models.BooleanField()  # Record participant's consent.

      q = models.IntegerField(label="", min=0, max=20)

      quiz1_all = quiz1_question("1. If in the first round you decide to contribute 5 tokens and other group members contribute 10, 15, 20 respectively. "
                                 "Imagine that the computer program later randomly selects the player who contributes 20 as the fourth player, for whom the "
                                 "payoff-relevant decision is from "
                                 "the second round. And this player decides to contribute 10 when the average contribution of other players in the"
                                 " first round is 10. What's your final payoff?")

      quiz2_all = quiz2_question("2. If in the first round you decide to contribute 20 tokens and other group members contribute 0, 10, 5 respectively. "
                                 "Imagine that the computer program later randomly selects you as the fourth player, for whom the payoff-relevant decision "
                                 "is from the second round. In the second round, you decide to contribute 13 when the average contribution in the first "
                                 "round is 5. What's your final payoff?")

      quiz3_all = quiz3_question(
          "3. If in the first round you decide to contribute 0 tokens and other group members contribute 5, 10, 20 respectively."
            " Imagine that the experimenter later selects the player who contributes 20, for whom the payoff-relevant decision is his/her "
           "second round decision. And this player decides to contribute 7 when the average contribution of other players in the first round is 5. "
            "What's your final payoff?")

      quiz4_all = quiz4_question(
          "4. If in the first round you decide to contribute 15 tokens and other group members contribute 5, 10, 20 respectively."
            " Imagine that the experimenter later selects the your second round decision as the payoff-relevant decision. And in the second"
                                 " round, you decide to contribute 10 when the average contribution in the first round is 10."
                                 " What's your final payoff?")

      def quiz1_all_error_message(self, quiz1_all):
          if quiz1_all != 35:
             self.participant.vars['quiz'] = 0
             return 'Your answer for this question is incorrect. The correct answer is 35. This is because the fourth player' \
                    ' decides to contribute 20 in the first round and to contribute 10 in the second round if other players’ average contribution is 10 [(5+10+15)/3] ' \
                    'in the first round. The group’s ' \
                    'total contribution to the POOL is thus 5 + 10 +15 + 10 = 40. Each player’s earning from the POOL is thus 40*2/4 = 20. Your final payoff is ' \
                    '20 - 5 + 20 = 35.'

      def quiz2_all_error_message(self, quiz2_all):
          if quiz2_all != 21:
             self.participant.vars['quiz'] = 0
             return 'Your answer for this question is incorrect.  The correct answer is 21. ' \
                    'This is because your second round decision is the payoff-relevant decision. In this round you decide to contribute ' \
                    '13 when other players on average contributed 5 in the first round. The group total contribution is thus 0 + 13 + 5 +10 = 28.' \
                    ' Each individual earnings from the POOL is thus 28*2/4 = 14.  Your final payoff is 20 - 13 + 14 = 21.'

      def quiz3_all_error_message(self, quiz3_all):
          if quiz3_all != 31:
             return 'Your answer for this quesiton is incorrect. The correct answer is 31.' \
                    ' This is because the fourth player decides to contribute 20 in the first round' \
                    ' and to contribute 7 in the second round if other players’ average contribute is 5 in the first round. ' \
                    'The group’s total contribution to the POOL is thus 7 + 5 + 10 + 0 = 22. ' \
                    'Each player’s earning from the POOL is thus 22*2/4 = 11.'\
                    ' Your final payoff is 20 - 0 + 11 = 31.' \

      def quiz4_all_error_message(self, quiz4_all):
          if quiz4_all != 30:
              return 'Your answer for this question is incorrect. The correct answer is 30. This is because ' \
                     'your second round decision is the payoff-relevant decision.' \
                     ' In this round you decide to contirbute 10 when other players on average contributed 10 in the first round. ' \
                     'The group total contribution is thus 10 + 5 + 10 +15 = 40. ' \
                     'Each individual earnings from the project is thus 40*2/4 = 20.' \
                     'Your final payoff is 20 - 10 + 20 = 30.'
