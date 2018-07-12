from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants, Player, Subsession, Group, BaseSubsession
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import export


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

class PracticeEnd(Page):
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
		products_total = Constants.num_products[self.subsession.block - 1]
		productdims_total = Constants.productdims_total[self.subsession.block - 1]
		productdims_shown = Constants.productdims_shown[self.subsession.block - 1]

		productdimvals = self.session.vars["productdims_round" + str(self.round_number)]
		productdimvals_shown = self.session.vars["productdims_shown_round" + str(self.round_number)]
		productdimvals_reversed = list(map(list, zip(*productdimvals_shown)))

		preferencedims = self.session.vars["preferencedims_round" + str(self.round_number)]

		products_list = list(range(1, products_total + 1))
		productdims_list = list(range(1, productdims_shown + 1))

		treatmentorder = list(map(int, self.session.config['treatmentorder'].split(',')))
		treatmentorder = [i - 1 for i in treatmentorder]

		num_rounds_treatment = [Constants.num_rounds_treatment[i] for i in treatmentorder]
		num_rounds_practice = [Constants.num_rounds_practice[i] for i in treatmentorder]

		numpracticerounds = sum(num_rounds_practice[:self.subsession.block])
		numtreatrounds = sum(num_rounds_treatment[:self.subsession.block])
		roundnum = self.subsession.round_number - numpracticerounds



		product_dims = []
		if self.subsession.practiceround:
			pass
			# product_dims = self.participant.vars["practice_proddims" + str(self.subsession.round_number)]
		else:
			for i in range(self.subsession.products):
				pass
		# 		product_dims.append([pd.value for pd in self.group.get_player_by_role(role).get_ask().productdim_set.all()])


		# products = list(zip(range(1, self.subsession.productdims_total + 1), zip(*product_dims)))
		return {
			"products_total": products_total,
			"productdims_total": productdims_total,
			"productdims_shown": productdims_shown,

			"productdimvals": productdimvals,
			"productdimvals_shown": productdimvals_shown,  # number of product dims shown
			"productdimvals_reversed": productdimvals_reversed,

			"products_list": products_list,
			"productdims_list": productdims_list,

			"treatmentorder": treatmentorder,
			"treatmentrounds": Constants.num_rounds_treatment[self.subsession.block - 1],

			"numpracticerounds": numpracticerounds,
			"numtreatrounds": numtreatrounds,
			"roundnum": roundnum,



			"practicerounds": Constants.num_rounds_practice[self.subsession.block - 1],
			"preferencedims": preferencedims,
			"practice_round:": self.subsession.practiceround,

		}

	def before_next_page(self):
		pass
		# product_choice = self.get_product_by_id("Prod" + str(self.player.product_selected))
		# productdims = [pd.value for pd in ask.productdim_sell.all()]
		# if self.subsession.practiceround:
		# 	self.participant.vars["practice_proddims" + str(self.subsession.round_number)] = [[0] * self.subsession.productdims_total for i in range(self.subsession.num_products)]
		# else:
		# 	self.participant.vars["proddims" + str(self.subsession.round_number)] = [[0] * self.subsession.productdims_total for i in range(self.subsession.num_products)]



class RoundResults(Page):
	def vars_for_template(self):

		productdimvals = self.session.vars["productdims_round" + str(self.round_number)]


		# if self.subsession.practiceround:
		# 	products = self.participant.vars["practice_proddims" + str(self.subsession.round_number)]
		# 	# if self.subsession.is_asl:
		# else:
		# 	products = self.participant.vars["proddims" + str(self.subsession.round_number)]
		# 	preferences = self
			# if self.subsession.is_asl:
				
		product_dims = []
		preferencedims = []
        # product_choice = player.product_selected
		# product_choice = self.participant.vars["product_selected" + str(self.subsession.round_number)]
		# Create a list of lists where each individual list is product dimension i for all products
		# for i in range(self.subsession.num_products):
		# 	product = "Prod" + str(i + 1)
			# product_dims.append([pd.value for pd in self.get]) TODO: finish this line using general_dimensions views line 376

		# products_list = list(zip(range(1, self.subsession.productdims_total + 1), zip(*product_dims)))
		return {
			"productdimvals": productdimvals,
		}
class ChoiceASL(Page):
	form_model = models.Player
	form_fields = ['product_selected']

	def is_displayed(self):
		return self.subsession.is_asl

	def vars_for_template(self):
		products_total = Constants.num_products[self.subsession.block - 1]
		productdims_total = Constants.productdims_total[self.subsession.block - 1]
		productdims_shown = Constants.productdims_shown[self.subsession.block - 1]

		productdimvals = self.session.vars["productdims_round" + str(self.round_number)]
		productdimvals_shown = self.session.vars["productdims_shown_round" + str(self.round_number)]
		preferencedims = self.session.vars["preferencedims_round" + str(self.round_number)]

		products_list = list(range(1, product_total + 1))
		productdims_list = list(range(1, productdims_shown + 1))
		productdims_reversed = list(map(list, zip(*productdims_shown)))

		treatmentorder = list(map(int, self.session.config['treatmentorder'].split(',')))
		treatmentorder = [i - 1 for i in treatmentorder]

		numpracticerounds = sum(Constants.num_rounds_practice[:self.subsession.block])
		numtreatrounds = sum(num_rounds_treatment[:self.subsession.block])
		roundnum = self.subsession.round_number - numpracticerounds


@login_required
def ViewData(request):
	return render(request, 'tiered_disclosure/adminData.html', {"session_code": Session.objects.last().code})

@login_required
def DataDownload(request):
	headers, body = export.export_contracts()
	return export.export_csv("Data", headers, body)

# page_sequence = [
#     InstructionsBasics,
#     InstructionsBasicsQuiz,
#     InstructionsASL,
#     InstructionsASLQuiz,
#     InstructionsTruncation,
#     InstructionsTruncationQuiz,
#     InstructionsNewTreatment,
#     InstructionsRoundResultsQuiz,
#     PracticeBegin,
#     PracticeEnd,
#     ChoiceTruncation,
#     ChoiceASL,
#     RoundResults,
# ]

page_sequence = [
    ChoiceTruncation,
    ChoiceASL,
    RoundResults,
]