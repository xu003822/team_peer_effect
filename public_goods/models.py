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


doc = """
This is a one-period public goods game with 3 players.
"""


class Constants(BaseConstants):
    name_in_url = 'public_goods_individual_treatment'
    players_per_group = 3
    num_rounds = 1

    instructions_template = 'public_goods_individual_treatment/instructions.html'

    # """Amount allocated to each player"""
    endowment = c(100)
    multiplier = 2


class Subsession(BaseSubsession):
    def vars_for_admin_report(self):
        contributions = [
            p.contribution for p in self.get_players() if p.contribution != None
        ]
        if contributions:
            return dict(
                avg_contribution=sum(contributions) / len(contributions),
                min_contribution=min(contributions),
                max_contribution=max(contributions),
            )
        else:
            return dict(
                avg_contribution='(no data)',
                min_contribution='(no data)',
                max_contribution='(no data)',
            )


class Group(BaseGroup):
    total_contribution = models.CurrencyField()

    individual_share = models.CurrencyField()

    def set_payoffs(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.individual_share = (
            self.total_contribution * Constants.multiplier / Constants.players_per_group
        )
        for p in self.get_players():
            p.payoff = (Constants.endowment - p.contribution) + self.individual_share


class Player(BasePlayer):
    contribution = models.CurrencyField(
        min=0, max=Constants.endowment, doc="""The amount contributed by the player""",
        label="How much will you contribute to the project (from 0 to 100)?"
    )

def quiz1_question(label):
    return models.IntegerField(
        choices = [14, 20, 24, 30],
        widget = widgets.RadioSelect,
        label = label
    )

def quiz2_question(label):
    return models.IntegerField(
        choices = [4, 6, 12, 20],
        widget = widgets.RadioSelect,
        label = label
    )

quiz1_all = quiz1_question("1. Suppose you contribute 10 tokens in this round and your group mates altogether contribute 30 tokens. How many tokens you will get at the end of this round?")
quiz2_all = quiz2_question("2. Suppose you contribute 20 tokens in this round and your group mates altogether contribute 40 tokens. How many tokens you will get at the end of this round?")
