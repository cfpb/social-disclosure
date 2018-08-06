# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants

class Risk1(Page):
    form_model = models.Player
    form_fields = ['q_risk1']

# Questions 2 and 3 are conditional on the first response
class Risk2(Page):
    form_model = models.Player
    form_fields = ['q_risk2']
    def is_displayed(self):
        return self.player.q_risk1 == 1
    def before_next_page(self):
        self.player.set_risk()
class Risk3(Page):
    form_model = models.Player
    form_fields = ['q_risk3']
    def is_displayed(self):
        return self.player.q_risk1 == 2
    def before_next_page(self):
        self.player.set_risk()

class Risk4(Page):
    form_model = models.Player
    form_fields = ['q_risk4']
    



class SubjNumeracy1(Page):
    form_model = models.Player
    form_fields = ['q_subjNum1', 'q_subjNum2', 'q_subjNum3']
class SubjNumeracy2(Page):
    form_model = models.Player
    form_fields = ['q_subjNum4','q_subjNum5', 'q_subjNum6']
class SubjNumeracy3(Page):
    form_model = models.Player
    form_fields = ['q_subjNum7', 'q_subjNum8']



class ObjNumeracy(Page):
    form_model = models.Player
    form_fields = ['q_objNum1', 'q_objNum2', 'q_objNum3' ]


class NFC1(Page):
    form_model = models.Player
    form_fields = ['q_nfc1', 'q_nfc2', 'q_nfc3']
class NFC2(Page):
    form_model = models.Player
    form_fields = ['q_nfc4', 'q_nfc5', 'q_nfc6']
class NFC3(Page):
    form_model = models.Player
    form_fields = ['q_nfc7', 'q_nfc8']


class Demographics1(Page):
    form_model = models.Player
    form_fields = ['q_experience', 'q_gender', 'q_english', 'q_age']
class Demographics2(Page):
    form_model = models.Player
    form_fields = ['q_course_micro', 'q_course_mkt', 'q_course_law']
    #def vars_for_template(self):
    #  return {'q_course_micro', 'q_course_mkt', 'q_course_law'}


# class FutureStudies(Page):
#     form_model = models.Player
#     form_fields = ['q_futureStudies']

class Splash(Page):
    form_model = models.Player
    form_fields = [ ]


page_sequence = [
    Risk1,Risk2,Risk3,Risk4,
    NFC1,NFC2,NFC3,
    SubjNumeracy1,SubjNumeracy2,SubjNumeracy3,
    ObjNumeracy,
    Demographics1,Demographics2,
    #FutureStudies,
    Splash
]
