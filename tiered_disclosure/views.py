from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants, Player, Subsession, Group, BaseSubsession
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import export

class Page1(Page):
    def before_next_page(self):
        pass

class InstructionsPage(Page):
    def is_displayed(self):
        return self.subsession.show_instructions_base

    def vars_for_template(self):
        return {
            'tokens_per_dollar': int(1./float(self.session.config["real_world_currency_per_point"])),
            'showup': self.session.config['participation_fee'],
        }

class InstructionsBasicsQuiz(Page):
	form_model = models.Player
	form_fields = ['basics_q1']

	def is_displayed(self):
		return	self.subsession.show_instructions_base

	def vars_for_template(self):
		return {
		    'tokens_per_dollar': int(1. / float(self.session.config["real_world_currency_per_point"])),
		}

class PracticeBegin(Page):
    def is_displayed(self):
        return self.subsession.show_instructions_practice

    def vars_for_template(self):
        practicerounds = Constants.num_rounds_practice[self.subsession.block - 1]
        return {
            "practicerounds": practicerounds

        }

class InstructionsTruncation(Page):
	def is_displayed(self):
		return self.subsession.show_instructions_truncation

	def vars_for_template(self):
		return {
				"products": range(1, self.subsession.products + 1),
			}

class ChoiceTruncation(Page):
	form_model = models.Player
	form_fields = ['product_selected']

	def is_displayed(self):
		return self.subsession.is_asl == 0

	def vars_for_template(self):
		treatmentorder = list(map(int, self.session.config['treatmentorder'].split(',')))
		treatmentorder = [i - 1 for i in treatmentorder]
		num_rounds_treatment = [Constants.num_rounds_treatment[i] for i in treatmentorder]
		#num_rounds_practice = [Constants.num_rounds_practice[i] for i in treatmentorder]
		
		numpracticerounds = sum(Constants.num_rounds_practice[:self.subsession.block])
		numtreatrounds = sum(num_rounds_treatment[:self.subsession.block])
		roundnum = self.subsession.round_number - numpracticerounds
		
		# product_dims = []
		# if self.subsession.practiceround:
		# 	productdims = self.participant.vars["practice_proddims" + str(self.subsession.round_number)]
		# else:
		# 	for i in range(self.subsession.products):
		# 		product_dims.append([pd.value for pd in self.group.get_player_by_role(role).get_ask().productdim_set.all()])

		product_total = Constants.num_products[self.subsession.block - 1]

		productdims = self.session.vars["products_round" + str(self.round_number)]
		preferencedims = self.session.vars["preferences_round" + str(self.round_number)]

		products = list(range(1, product_total + 1))
		# products = list(zip(range(1, self.subsession.productdims_total + 1), zip(*product_dims)))
		return {
			"products": products,
			"producttotal": product_total,
			"round": roundnum,
			"numpracticerounds": numpracticerounds,
			"numtreatrounds": numtreatrounds,

			"productdims": productdims,
			
			"treatmentorder": list(map(int, self.session.config['treatmentorder'].split(','))),
			"treatmentrounds": Constants.num_rounds_treatment[self.subsession.block - 1],
			"practicerounds": Constants.num_rounds_practice[self.subsession.block - 1],
			"total_productdims": Constants.productdims_total[self.subsession.block - 1],
			"shown_productdims": Constants.productdims_shown[self.subsession.block - 1],
			"preferencedims": preferencedims,
			"practice_round:": self.subsession.practiceround
		}

	# def before_next_page(self):
 #        """ Create bid object.  Set buyer price attributes """
 #        # if self.subsession.practiceround:
 #        #     self.participant.vars["practice_bids" + str(self.subsession.round_number)] = [[0] * self.subsession.sellers for i in range(self.subsession.buyers)]
 #        #     self.participant.vars["practice_bids" + str(self.subsession.round_number)][0][self.player.contract_seller_rolenum - 1] = 1
 #        #     for sellers in self.participant.vars["practice_bids" + str(self.subsession.round_number)]:
 #        #         if sum(sellers) == 0:
 #        #             sellers[random.randint(1, self.subsession.sellers) - 1] = 1
 #        #     buyer_choices = self.participant.vars["practice_bids" + str(self.subsession.round_number)]
 #        #     items_sold = list(map(sum, zip(*buyer_choices)))[0]
 #        #     price = sum(self.participant.vars["practice_asks" + str(self.subsession.round_number)][self.player.contract_seller_rolenum - 1])
 #        #     self.player.payoff_marginal = Constants.consbenefit - price
 #        #     self.player.bid_total = price
 #        # else:
 #        	product = ("Prod" + str(self.player.contract_seller_rolenum))
 #        	# productdims = [pd.value for pd in ]

 #            bid = self.player.create_bid(ask.total, pricedims)

 #            self.group.create_contract(bid=bid, ask=ask)
 #            self.player.set_buyer_data()
@login_required
def ViewData(request):
	return render(request, 'tiered_disclosure/adminData.html', {"session_code": Session.objects.last().code})

@login_required
def DataDownload(request):
	headers, body = export.export_contracts()
	return export.export_csv("Data", headers, body)

page_sequence = [
    InstructionsPage,
    InstructionsBasicsQuiz,
    PracticeBegin,
    ChoiceTruncation
]
