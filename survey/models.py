# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer

from otree import widgets
from otree.common import Currency as c, currency_range
import random
# </standard imports>

from django_countries.fields import CountryField


class Constants(BaseConstants):
    name_in_url = 'survey'
    players_per_group = None
    num_rounds = 1
    nfc_responses = [ [1, 'Extremely uncharacteristic of me'],
                  [2, 'Somewhat uncharacteristic of me'],
                  [3, 'Uncertain'],
                  [4, 'Somewhat characteristic of me'],
                  [5, 'Extremely characteristic of me'] ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    q_risk1 = models.PositiveIntegerField(
        initial=None,
        blank=True,
        choices=[
            [1, 'A 50% chance of $35'],
            [2, 'A 100% chance of $15'] ],
        verbose_name='Hypothetically, which would you prefer: a 50% chance of getting $35 or a 100% chance of getting $15?',
        widget=widgets.RadioSelect())
    q_risk2 = models.PositiveIntegerField(
        initial=None,
        blank=True,
        choices=[
            [1, 'A 50% chance of $35'], 
            [2, 'A 100% chance of $17.50']],
        verbose_name='Hypothetically, which would you prefer: a 50% chance of getting $35 or a 100% chance of getting $17.50?',
        widget=widgets.RadioSelect())
    q_risk3 = models.PositiveIntegerField(
        initial=None,
        blank=True,
        choices=[
            [1, 'A 50% chance of $35'],
            [2, 'A 100% chance of $10']],
        verbose_name='Hypothetically, which would you prefer: a 50% chance of getting $35 or a 100% chance of getting $10?',
        widget=widgets.RadioSelect())
    q_risk4 = models.PositiveIntegerField(
        initial=None,
        blank=True,
        choices=[
            [1, '1. Not at all willing to take risks'],
            [2, '2'],
            [3, '3'],
            [4, '4'],
            [5, '5. Very willing to take risks']],
        verbose_name='How willing are you to take risks in your life, in general?',
        widget=widgets.RadioSelect())

    riskaverse_1 = models.BooleanField(default=False, doc="Risk Seeking. True if q_risk1==1 and q_risk2==1")
    riskaverse_2 = models.BooleanField(default=False, doc="Risk Neutral. True if q_risk1==1 and q_risk2==2")
    riskaverse_3 = models.BooleanField(default=False, doc="Risk Averse. True if q_risk1==2 and q_risk3==1")
    riskaverse_4 = models.BooleanField(default=False, doc="Risk Averse, Strong. True if q_risk1==2 and q_risk3==2")

    q_subjNum1 = models.PositiveIntegerField(
        initial=None,
        blank=True,
        choices=[
            [1, '1. Not at all good'],
            [2, '2'],
            [3, '3'],
            [4, '4'],
            [5, '5'],
            [6, '6. Extremely good']],
        verbose_name='How good are you at working with fractions?',
        widget=widgets.RadioSelect())
    q_subjNum2 = models.PositiveIntegerField(
        initial=None,
        blank=True,
        choices=[
            [1, '1. Not at all good'],
            [2, '2'],
            [3, '3'],
            [4, '4'],
            [5, '5'],
            [6, '6. Extremely good']],
        verbose_name='How good are you at working with percentages?',
        widget=widgets.RadioSelect())
    q_subjNum3 = models.PositiveIntegerField(
        initial=None,
        blank=True,
        choices=[
            [1, '1. Not at all good'],
            [2, '2'],
            [3, '3'],
            [4, '4'],
            [5, '5'],
            [6, '6. Extremely good']],
        verbose_name='How good are you at calculating a 15% tip?',
        widget=widgets.RadioSelect())
    q_subjNum4 = models.PositiveIntegerField(
        initial=None,
        blank=True,
        choices=[
            [1, '1. Not at all good'],
            [2, '2'],
            [3, '3'],
            [4, '4'],
            [5, '5'],
            [6, '6. Extremely good']],
        verbose_name='How good are you at figuring out how much a shirt will cost if it is 25% off?',
        widget=widgets.RadioSelect())
    q_subjNum5 = models.PositiveIntegerField(
        initial=None,
        blank=True,
        choices=[
            [1, '1. Not at all'],
            [2, '2'],
            [3, '3'],
            [4, '4'],
            [5, '5'],
            [6, '6. Extremely']],
        verbose_name='When reading the newspaper, how helpful do you find tables and graphs that are parts of a story?',
        widget=widgets.RadioSelect())
    q_subjNum6 = models.PositiveIntegerField(
        initial=None,
        blank=True,
        choices=[
            [1, '1. Always prefer words'],
            [2, '2'],
            [3, '3'],
            [4, '4'],
            [5, '5'],
            [6, '6. Always prefer numbers']],
        verbose_name='When people tell you the chance of something happening, do you prefer that they use words ("it rarely happens") or numbers ("there\'s a 1% chance")?',
        widget=widgets.RadioSelect())
    q_subjNum7 = models.PositiveIntegerField(
        initial=None,
        blank=True,
        choices=[
            [1, '1. Always prefer percentages'],
            [2, '2'],
            [3, '3'],
            [4, '4'],
            [5, '5'],
            [6, '6. Always prefer words']],
        verbose_name='When you hear a weather forecast, do you prefer predictions using percentages (e.g., "there will be a 20% chance of rain today") or predictions using only words (e.g., "there is a small chance of rain today")?',
        widget=widgets.RadioSelect())
    q_subjNum8 = models.PositiveIntegerField(
        initial=None,
        blank=True,
        choices=[
            [1, '1. Never'],
            [2, '2'],
            [3, '3'],
            [4, '4'],
            [5, '5'],
            [6, '6. Very often']],
        verbose_name='How often do you find numerical information to be useful?',
        widget=widgets.RadioSelect())

    q_objNum1 = models.PositiveIntegerField(
        verbose_name='Imagine that we have a fair, 6-sided die (for example, from a board game or a casino craps table).  Imagine we now roll it 1000 times.  Out of 1000 rolls, how many times do you think the die would come up even (numbers 2, 4, or 6)?',
        blank=True,
        min=0,
        max=10000,
        initial=None)
    q_objNum2 = models.PositiveIntegerField(
        verbose_name='In the Big Bucks Lottery, the chance of winning a $10.00 prize is 1%.  What is your best guess about how many people would win a $10.00 prize if 1000 people each buy a single ticket to Big Bucks?',
        blank=True,
        min=0,
        max=10000,
        initial=None)
    q_objNum3 = models.DecimalField(
        verbose_name='In the Acme Publishing Sweepstakes, the chance of winning a car is 1 in 1000.  What percentage of tickets to Acme Publishing Sweepstakes win a car?',
        blank=True,
        max=10000,
        max_digits=5,
        decimal_places=3,
        initial=None)

    q_nfc1 = models.PositiveIntegerField(
        initial=None,
        blank=True,
        choices=Constants.nfc_responses,
        verbose_name='I would prefer complex to simple problems.',
        widget=widgets.RadioSelect())
    q_nfc2 = models.PositiveIntegerField(
        initial=None,
        blank=True,
        choices=Constants.nfc_responses,
        verbose_name='I like to have the responsibility of handling a situation that requires a lot of thinking.',
        widget=widgets.RadioSelect())
    q_nfc3 = models.PositiveIntegerField(
        initial=None,
        blank=True,
        choices=Constants.nfc_responses,
        verbose_name='Thinking is not my idea of fun.',
        widget=widgets.RadioSelect())
    q_nfc4 = models.PositiveIntegerField(
        initial=None,
        blank=True,
        choices=Constants.nfc_responses,
        verbose_name='I would rather do something that requires little thought than something that is sure to challenge my thinking abilities.',
        widget=widgets.RadioSelect())
    q_nfc5 = models.PositiveIntegerField(
        initial=None,
        blank=True,
        choices=Constants.nfc_responses,
        verbose_name='I find satisfaction in deliberating hard and for long hours.',
        widget=widgets.RadioSelect())
    q_nfc6 = models.PositiveIntegerField(
        initial=None,
        blank=True,
        choices=Constants.nfc_responses,
        verbose_name='I only think as hard as I have to.',
        widget=widgets.RadioSelect())
    q_nfc7 = models.PositiveIntegerField(
        initial=None,
        blank=True,
        choices=Constants.nfc_responses,
        verbose_name='I prefer my life to be filled with puzzles I must solve.',
        widget=widgets.RadioSelect())
    q_nfc8 = models.PositiveIntegerField(
        initial=None,
        blank=True,
        choices=Constants.nfc_responses,
        verbose_name='I feel relief rather than satisfaction after completing a task that requires a lot of mental effort.',
        widget=widgets.RadioSelect())

    q_experience = models.CharField(
        initial=None,
        blank=True,
        choices=['0', '1 to 3', '4 to 6', '7 to 9', '10 or more'],
        verbose_name='Approximately how many in-person, laboratory experiments have you completed before today?  If you\'re not sure, please make your best guess.',
        widget=widgets.RadioSelect())
    q_english = models.CharField(
        initial=None,
        blank=True,
        choices=['Yes', 'No', 'Prefer not to answer'],
        verbose_name='Is English your primary language?',
        widget=widgets.RadioSelect())
    q_gender = models.CharField(
        initial=None,
        blank=True,
        choices=['Male', 'Female', 'Other'],
        verbose_name='What is your gender?',
        widget=widgets.RadioSelect())
    q_age = models.PositiveIntegerField(
        verbose_name='How old are you, in years?',
        blank=True,
        min=16,
        max=120,
        initial=None)

    q_course_micro = models.BooleanField(blank=True)
    q_course_mkt   = models.BooleanField(blank=True)
    q_course_law   = models.BooleanField(blank=True)

    # q_futureStudies = models.CharField(
    #     initial=None,
    #     choices=['Yes, I would like to be contacted for future studies', 'No, I would not like to be contacted for future studies'],
    #     verbose_name='Researchers conducting this study may be interested in contacting you regarding additional research studies in the next year.  These future studies will provide compensation of approximately $35/hour.  Please indicate whether you would like us to contact you for these studies.  Doing so will not affect any aspect of your participation today, including payment or privacy.',
    #     widget=widgets.RadioSelect())

    def set_risk(self):
        """ Aggregates risk responses into categories """
        self.riskaverse_1 = True if self.q_risk1==1 and self.q_risk2==1 else False
        self.riskaverse_2 = True if self.q_risk1==1 and self.q_risk2==2 else False
        self.riskaverse_3 = True if self.q_risk1==2 and self.q_risk3==1 else False
        self.riskaverse_4 = True if self.q_risk1==2 and self.q_risk3==2 else False