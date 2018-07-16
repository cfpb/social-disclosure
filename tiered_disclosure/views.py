from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants, Player, Subsession, Group, BaseSubsession
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import export
import string

class InstructionsTruncation(Page):
	def is_displayed(self):
		return self.subsession.show_instructions_truncation

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


class ChoiceTruncation(Page):
	form_model = models.Player
	form_fields = ['product_selected']

	def is_displayed(self):
		return self.subsession.is_asl == 0

	def vars_for_template(self):
		products_total = Constants.num_products[self.subsession.block - 1]
		productdims_total = Constants.productdims_total[self.subsession.block - 1]
		productdims_shown = Constants.productdims_shown[self.subsession.block - 1]

		preferencedims = Constants.num_prefdims[self.subsession.block - 1]

		productdimvals = self.session.vars["productdims_round" + str(self.round_number)]
		productdimvals_shown = self.session.vars["productdims_shown_round" + str(self.round_number)]
		# productdimvals_selected = productdimvals[player.product_selected]

		productdimvals_transposed = list(map(list, zip(*productdimvals_shown)))

		preferencedimvals = self.session.vars["preferencedims_round" + str(self.round_number)]
		preferencedimvals_transposed = list(map(list, zip(*preferencedimvals)))

		products_list = list(range(1, products_total + 1))
		productdims_list = list(range(1, productdims_shown + 1))

		preferences_list = list(range(1, preferencedims + 1))

		treatmentorder = list(map(int, self.session.config['treatmentorder'].split(',')))
		treatmentorder = [i - 1 for i in treatmentorder]

		num_rounds_treatment = [Constants.num_rounds_treatment[i] for i in treatmentorder]
		num_rounds_practice = [Constants.num_rounds_practice[i] for i in treatmentorder]

		numpracticerounds = sum(num_rounds_practice[:self.subsession.block])
		numtreatrounds = sum(num_rounds_treatment[:self.subsession.block])
		treatmentroundnum = self.subsession.round_number - numpracticerounds

		product_dims = []
		if self.subsession.practiceround:
			pass
			# product_dims = self.participant.vars["practice_proddims" + str(self.subsession.round_number)]
		# else:
			# for i in range(self.subsession.numproducts):
		# 		product_dims.append([pd.value for pd in self.group.get_player_by_role(role).get_ask().productdim_set.all()])

		maxprefdim = max(Constants.num_prefdims)
		maxproduct = max(Constants.num_products)
		maxproductdim = max(Constants.productdims_total)

		d = dict(enumerate(string.ascii_uppercase, 1))  # converts number to alphabet
		prefdim_fns = [str(d[i]) for i in range(1, maxprefdim + 1)]
		proddim_fns = [str(d[j]) for j in range(1, maxproductdim + 1)]

		# self.participant.vars["product_selected" + str(self.subsession.round_number)]
		# products = list(zip(range(1, self.subsession.productdims_total + 1), zip(*product_dims)))
		return {
			"products_total": products_total,
			"productdims_total": productdims_total,
			"productdims_shown": productdims_shown,

			"productdimvals": productdimvals,
			"productdimvals_shown": productdimvals_shown,  # number of product dims shown
			"productdimvals_transposed": productdimvals_transposed,
			# "productdimvals_selected": productdimvals_selected,

			"preferencedimvals": preferencedimvals,
			"preferenceddimvals_transposed": preferencedimvals_transposed,

			# "products_dict": products_dict,

			"products_list": products_list,
			"productdims_list": productdims_list,

			"preferences_list": preferences_list,

			"treatmentorder": treatmentorder,
			"treatmentrounds": Constants.num_rounds_treatment[self.subsession.block - 1],

			# "numpracticerounds": numpracticerounds,
			"numtreatrounds": numtreatrounds,
			"treatmentroundnum": treatmentroundnum,


			"preferencedims": preferencedims,

			"practicerounds": Constants.num_rounds_practice[self.subsession.block - 1],
			"practice_round:": self.subsession.practiceround,

			"prefdim_fns": prefdim_fns,
			"proddim_fns": proddim_fns,
		}

	def before_next_page(self):
		# self.player.product_selected_dims = self.session.vars["productdims_round" + str(self.round_number)][self.player.product_selected]
		pass
		# product_choice = self.get_product_by_id("Prod" + str(self.player.product_selected))
		# productdims = [pd.value for pd in ask.productdim_sell.all()]
		# if self.subsession.practiceround:
		# 	self.participant.vars["practice_proddims" + str(self.subsession.round_number)] = [[0] * self.subsession.productdims_total for i in range(self.subsession.num_products)]
		# else:
		# 	self.participant.vars["proddims" + str(self.subsession.round_number)] = [[0] * self.subsession.productdims_total for i in range(self.subsession.num_products)]



class RoundResults(Page):
	def vars_for_template(self):
		product_selected = self.player.product_selected
		productdimvals = self.session.vars["productdims_round" + str(self.round_number)]
		if self.subsession.is_asl == 0:
			productdimvals_shown = self.session.vars["productdims_shown_round" + str(self.round_number)]
			productdims_shown = Constants.productdims_shown[self.subsession.block - 1]

		productdimvals_selected = self.session.vars["productdims_round" + str(self.round_number)][product_selected - 1]

		products_total = Constants.num_products[self.subsession.block - 1]
		productdims_total = Constants.productdims_total[self.subsession.block - 1]

		# productdimvals_selected = productdimvals[player.product_selected]
		productdimvals_transposed = list(map(list, zip(*productdimvals)))
		# productdimvalsshown_transposed = list(map(list, zip(*productdimvals_shown)))

		preferencedims = self.session.vars["preferencedims_round" + str(self.round_number)]

		products_list = list(range(1, products_total + 1))
		# productdims_list = list(range(1, productdims_shown + 1))
		# if self.subsession.practiceround:
		# 	products = self.participant.vars["practice_proddims" + str(self.subsession.round_number)]
		# 	# if self.subsession.is_asl:
		# else:
		# 	products = self.participant.vars["proddims" + str(self.subsession.round_number)]
		# 	preferences = self
			# if self.subsession.is_asl:


        # product_choice = player.product_selected
		# product_choice = self.participant.vars["product_selected" + str(self.subsession.round_number)]
		# Create a list of lists where each individual list is product dimension i for all products
		# for i in range(self.subsession.num_products):
		# 	product = "Prod" + str(i + 1)
			# product_dims.append([pd.value for pd in self.get]) TODO: finish this line using general_dimensions views line 376

		# products_list = list(zip(range(1, self.subsession.productdims_total + 1), zip(*product_dims)))
		return {
			"product_selected": product_selected,
			"productdimvals": productdimvals,
			"productdimvals_selected": productdimvals_selected,

			"products_total": products_total,
			"productdims_total": productdims_total,

			"products_list": products_list,

			"preferencedims": preferencedims,

			"productdimvals": productdimvals,
			"productdimvals_transposed": productdimvals_transposed,
		}

class ChoiceASL(Page):
	form_model = models.Player
	form_fields = ['product_selected']

	def is_displayed(self):
		return self.subsession.is_asl

	def vars_for_template(self):
		products_total = Constants.num_products[self.subsession.block - 1]
		productdims_total = Constants.productdims_total[self.subsession.block - 1]
		representativedimvals = self.session.vars["productdims_round" + str(self.round_number)]
		preferencedims = self.session.vars["preferencedims_round" + str(self.round_number)]
		productdims_total = Constants.productdims_total[self.subsession.block - 1]
		products_total = Constants.num_products[self.subsession.block - 1]

		num_representatives = Constants.num_representatives[self.subsession.block - 1]
		num_preferences = Constants.num_prefdims[self.subsession.block - 1]

		utility_dims = self.session.vars["reputility_round" + str(self.round_number)]
		representatives_list = list(range(1, num_representatives + 1))
		preferences_list = list(range(1, num_preferences + 1))

		representativedimvals_transposed = list(map(list, zip(*representativedimvals)))

		treatmentorder = list(map(int, self.session.config['treatmentorder'].split(',')))
		treatmentorder = [i - 1 for i in treatmentorder]
		products_list = list(range(1, products_total + 1))

		# numpracticerounds = sum(Constants.num_rounds_practice[:self.subsession.block])
		return {
			"num_representatives": num_representatives,
			"representativedimvals": representativedimvals,
			"utility_dims": utility_dims,

			"products_total": products_total,
			"productdims_total": productdims_total,
			"products_list": products_list,
			"representativedimvals_transposed": representativedimvals_transposed,
			"representatives_list": representatives_list,
			"preferences_list": preferences_list,

			"preferencedims": preferencedims,
		}

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