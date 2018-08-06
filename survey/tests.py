# -*- coding: utf-8 -*-
from __future__ import division
import random
from otree.common import Currency as c, currency_range
from otree.api import Submission
from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    # Bot chooses randomly from survey response options
    def play_round(self):
        risk1_answer = random.choice([1,2])
        yield(views.Risk1, {"q_risk1" : risk1_answer})
        if (risk1_answer == 1):
            yield(views.Risk2, {"q_risk2" : random.choice(['A 50% chance of $35', 'A 100% chance of $17.50'])})
        if (risk1_answer == 2):
            yield(views.Risk3, {"q_risk3" : random.choice(['A 50% chance of $35', 'A 100% chance of $10'])})
        yield(views.Risk4, {"q_risk4" : random.choice(['1. Not at all willing to take risks', '2', '3', '4', '5. Very willing to take risks'])})
        yield(views.NFC1, {"q_nfc1" : random.randint(1,5), "q_nfc2" : random.randint(1,5), "q_nfc3" : random.randint(1,5)})
        yield(views.NFC2, {"q_nfc4" : random.randint(1,5), "q_nfc5" : random.randint(1,5), "q_nfc6" : random.randint(1,5)})
        yield(views.NFC3, {"q_nfc7" : random.randint(1,5), "q_nfc8" : random.randint(1,5)})
        yield(views.SubjNumeracy1, {'q_subjNum1' : random.choice(['1. Not at all good', '2', '3', '4', '5', '6. Extremely good']),
                                    'q_subjNum2' : random.choice(['1. Not at all good', '2', '3', '4', '5', '6. Extremely good']), 
                                    'q_subjNum3' : random.choice(['1. Not at all good', '2', '3', '4', '5', '6. Extremely good'])})
        yield(views.SubjNumeracy2, {'q_subjNum4' : random.choice(['1. Not at all good', '2', '3', '4', '5', '6. Extremely good']),
                                    'q_subjNum5' : random.choice(['1. Not at all', '2', '3', '4', '5', '6. Extremely']), 
                                    'q_subjNum6' : random.choice(['1. Always prefer words', '2', '3', '4', '5', '6. Always prefer numbers'])})
        yield(views.SubjNumeracy3, {'q_subjNum7' : random.choice(['1. Always prefer percentages', '2', '3', '4', '5', '6. Always prefer words']), 
                                    'q_subjNum8' : random.choice(['1. Never', '2', '3', '4', '5', '6. Very often'])})
        yield(views.ObjNumeracy, {'q_objNum1' : random.randint(0,10000), 'q_objNum2' : random.randint(0, 10000), 'q_objNum3' : round(random.random(), 3)})
        yield(views.Demographics1, {'q_experience' : random.choice(['0', '1 to 3', '4 to 6', '7 to 9', '10 or more']), 
                                    'q_gender' : random.choice(["Male", "Female"]), 
                                    'q_english' : random.choice(['Yes', 'No', 'Prefer not to answer']), 
                                    'q_age' : random.randint(16,120)})
        yield(views.Demographics2, {'q_course_micro' : random.choice([True, False]), 'q_course_mkt' : random.choice([True, False]), 'q_course_law' : random.choice([True, False])})
        yield(views.FutureStudies, {"q_futureStudies" : random.choice(['Yes, I would like to be contacted for future studies', 'No, I would not like to be contacted for future studies'])})
        yield Submission(views.Splash, check_html = False)




