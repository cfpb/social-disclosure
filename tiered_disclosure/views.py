from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants, Player, Subsession, Group, BaseSubsession
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import export
import string


class InstructionsBasics(Page):
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

class InstructionsFullInformation(Page):
	def is_displayed(self):
		return self.subsession.show_instructions_base

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
        return self.subsession.show_instructions_real

    def vars_for_template(self):
        treatmentrounds = Constants.num_rounds_treatment[self.subsession.block - 1]
        return {
            "treatmentrounds": treatmentrounds,
        }

class ChoiceFullInformation(Page):
	form_model = models.Player
	form_fields = ['product_selected']

	def is_displayed(self):
		return self.subsession.is_asl == 0

	def vars_for_template(self):
		products_total = Constants.num_products[self.subsession.block - 1]
		productdims_total = Constants.productdims_total[self.subsession.block - 1]
		productdims_shown = Constants.productdims_shown[self.subsession.block - 1]
		productdimvals = self.session.vars["productdims_round" + str(self.round_number)]
		productdimvals_transposed = list(map(list, zip(*productdimvals)))
		productdims_list = list(range(1, productdims_shown + 1))
		products_list = list(range(1, products_total + 1))

		preferencedims = Constants.num_prefdims[self.subsession.block - 1]
		preferencedimvals = self.session.vars["preferencedims_round" + str(self.round_number)]
		# preferencedimvals_transposed = list(map(list, zip(*preferencedimvals)))
		preferences_list = list(range(1, preferencedims + 1))

		treatmentorder = list(map(int, self.session.config['treatmentorder'].split(',')))
		treatmentorder = [i - 1 for i in treatmentorder]

		num_rounds_treatment = [Constants.num_rounds_treatment[i] for i in treatmentorder]
		num_rounds_practice = [Constants.num_rounds_practice[i] for i in treatmentorder]

		numpracticerounds = sum(num_rounds_practice[:self.subsession.block])
		numtreatrounds = sum(num_rounds_treatment[:self.subsession.block])
		treatmentroundnum = self.subsession.round_number - numpracticerounds
		numpracticerounds = sum(num_rounds_practice[:self.subsession.block])
		numtreatrounds = sum(Constants.num_rounds_treatment[:self.subsession.block - 1])
		
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
		roundnum = self.subsession.round_number - numpracticerounds - numtreatrounds
		# self.participant.vars["product_selected" + str(self.subsession.round_number)]
		# products = list(zip(range(1, self.subsession.productdims_total + 1), zip(*product_dims)))
		return {
			"products_total": products_total,
			"productdims_total": productdims_total,
			"productdims_shown": productdims_shown,

			"productdimvals": productdimvals,
			"productdimvals_transposed": productdimvals_transposed,

			"preferencedimvals": preferencedimvals,

			"products_list": products_list,
			"productdims_list": productdims_list,

			"preferences_list": preferences_list,

			"treatmentorder": treatmentorder,
			"treatmentrounds": Constants.num_rounds_treatment[self.subsession.block - 1],

			"numpracticerounds": numpracticerounds,
			"numtreatrounds": numtreatrounds,

			"treatmentrounds": Constants.num_rounds_treatment[self.subsession.block - 1],
			"treatmentroundnum": treatmentroundnum,

			"round_number": self.round_number,

			"preferencedims": preferencedims,

			"practicerounds": Constants.num_rounds_practice[self.subsession.block - 1],
			"practice_round:": self.subsession.practiceround,

			"prefdim_fns": prefdim_fns,
			"proddim_fns": proddim_fns,

			"round": roundnum,
            "treatmentrounds": Constants.num_rounds_treatment[self.subsession.block - 1],

            "block": self.subsession.block,
		}

	def before_next_page(self):
		pass
		# self.player.product_selected_dims = self.session.vars["productdims_round" + str(self.round_number)][self.player.product_selected]
		# product_choice = self.get_product_by_id("Prod" + str(self.player.product_selected))
		# productdims = [pd.value for pd in ask.productdim_sell.all()]
		# if self.subsession.practiceround:
		# 	self.participant.vars["practice_proddims" + str(self.subsession.round_number)] = [[0] * self.subsession.productdims_total for i in range(self.subsession.num_products)]
		# else:
		# 	self.participant.vars["proddims" + str(self.subsession.round_number)] = [[0] * self.subsession.productdims_total for i in range(self.subsession.num_products)]


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
		productdimvals_transposed = list(map(list, zip(*productdimvals_shown)))
		productdims_list = list(range(1, productdims_shown + 1))
		products_list = list(range(1, products_total + 1))

		preferencedims = Constants.num_prefdims[self.subsession.block - 1]
		preferencedimvals = self.session.vars["preferencedims_round" + str(self.round_number)]
		# preferencedimvals_transposed = list(map(list, zip(*preferencedimvals)))
		preferences_list = list(range(1, preferencedims + 1))

		treatmentorder = list(map(int, self.session.config['treatmentorder'].split(',')))
		treatmentorder = [i - 1 for i in treatmentorder]

		num_rounds_treatment = [Constants.num_rounds_treatment[i] for i in treatmentorder]
		num_rounds_practice = [Constants.num_rounds_practice[i] for i in treatmentorder]

		numpracticerounds = sum(num_rounds_practice[:self.subsession.block])
		numtreatrounds = sum(num_rounds_treatment[:self.subsession.block])
		treatmentroundnum = self.subsession.round_number - numpracticerounds
		numpracticerounds = sum(num_rounds_practice[:self.subsession.block])
		numtreatrounds = sum(Constants.num_rounds_treatment[:self.subsession.block - 1])
		
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
		roundnum = self.subsession.round_number - numpracticerounds - numtreatrounds
		# self.participant.vars["product_selected" + str(self.subsession.round_number)]
		# products = list(zip(range(1, self.subsession.productdims_total + 1), zip(*product_dims)))
		return {
			"products_total": products_total,
			"productdims_total": productdims_total,
			"productdims_shown": productdims_shown,

			"productdimvals": productdimvals,
			"productdimvals_shown": productdimvals_shown,  # number of product dims shown
			"productdimvals_transposed": productdimvals_transposed,

			"preferencedimvals": preferencedimvals,

			"products_list": products_list,
			"productdims_list": productdims_list,

			"preferences_list": preferences_list,

			"treatmentorder": treatmentorder,
			"treatmentrounds": Constants.num_rounds_treatment[self.subsession.block - 1],

			"numpracticerounds": numpracticerounds,
			"numtreatrounds": numtreatrounds,

			"treatmentrounds": Constants.num_rounds_treatment[self.subsession.block - 1],
			"treatmentroundnum": treatmentroundnum,

			"round_number": self.round_number,

			"preferencedims": preferencedims,

			"practicerounds": Constants.num_rounds_practice[self.subsession.block - 1],
			"practice_round:": self.subsession.practiceround,

			"prefdim_fns": prefdim_fns,
			"proddim_fns": proddim_fns,

			"round": roundnum,
            "treatmentrounds": Constants.num_rounds_treatment[self.subsession.block - 1],

            "block": self.subsession.block,
		}

	def before_next_page(self):
		pass
		# self.player.product_selected_dims = self.session.vars["productdims_round" + str(self.round_number)][self.player.product_selected]
		# product_choice = self.get_product_by_id("Prod" + str(self.player.product_selected))
		# productdims = [pd.value for pd in ask.productdim_sell.all()]
		# if self.subsession.practiceround:
		# 	self.participant.vars["practice_proddims" + str(self.subsession.round_number)] = [[0] * self.subsession.productdims_total for i in range(self.subsession.num_products)]
		# else:
		# 	self.participant.vars["proddims" + str(self.subsession.round_number)] = [[0] * self.subsession.productdims_total for i in range(self.subsession.num_products)]

class ChoiceASL(Page):
	form_model = models.Player
	form_fields = ['product_selected']

	def is_displayed(self):
		return self.subsession.is_asl

	def vars_for_template(self):
		products_total = Constants.num_products[self.subsession.block - 1]
		productdims_total = Constants.productdims_total[self.subsession.block - 1]
		representativedimvals = self.session.vars["representativedims_round" + str(self.round_number)]
		preferencedims = self.session.vars["preferencedims_round" + str(self.round_number)]
		productdims_total = Constants.productdims_total[self.subsession.block - 1]
		productdimvals = self.session.vars["productdims_round" + str(self.round_number)]

		products_total = Constants.num_products[self.subsession.block - 1]

		treatmentorder = list(map(int, self.session.config['treatmentorder'].split(',')))
		treatmentorder = [i - 1 for i in treatmentorder]
		num_rounds_treatment = [Constants.num_rounds_treatment[i] for i in treatmentorder]
		num_rounds_practice = [Constants.num_rounds_practice[i] for i in treatmentorder]
		
		numpracticerounds = sum(num_rounds_practice[:self.subsession.block])
		# treatmentrounds = Constants.num_rounds_treatment[self.subsession.block - 1]
		numtreatrounds = sum(Constants.num_rounds_treatment[:self.subsession.block - 1])

		# treatmentroundnum = self.subsession.round_number/self.subsession.block NEED TO MULTIPLY BY NUMBER OF PRACTICE ROUNDS THAT HVA EOCCURED

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
		roundnum = self.subsession.round_number - numpracticerounds - numtreatrounds

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
			# "treatmentrounds": treatmentrounds,
			# "treatmentroundnum": treatmentroundnum,
			"preferencedims": preferencedims,
			"block": self.subsession.block,

			"round": roundnum,
            "treatmentrounds": Constants.num_rounds_treatment[self.subsession.block - 1] 
		}
		def before_next_page(self):
			pass


class RoundResults(Page):
	def vars_for_template(self):
		product_selected = self.player.product_selected
		num_preferences = Constants.num_prefdims[self.subsession.block - 1]
		product_best = self.session.vars["bestproduct_round" + str(self.round_number)]
		is_mistake = -1
		preferences_list = list(range(1, num_preferences + 1))

		if product_selected == product_best:
			is_mistake = 0
		else:
			is_mistake = 1
		productdimvals_selected = self.session.vars["productdims_round" + str(self.round_number)][product_selected - 1]
		productdimvals_best = self.session.vars["productdims_round" + str(self.round_number)][product_best - 1]
		selected_utility = self.session.vars["productutilities_round" + str(self.round_number)][product_selected - 1]
		utilities_list = self.session.vars["productutilities_round" + str(self.round_number)] 
		productdimvals = self.session.vars["productdims_round" + str(self.round_number)]
		if self.subsession.is_asl == 1:
			num_representatives = Constants.num_representatives[self.subsession.block - 1]
			representatives_list = list(range(1, num_representatives + 1))
			representativedimvals = self.session.vars["productdims_round" + str(self.round_number)]
			representativedimvals_transposed = list(map(list, zip(*representativedimvals)))
		else:
			productdimvals_shown = self.session.vars["productdims_shown_round" + str(self.round_number)]
			productdims_shown = Constants.productdims_shown[self.subsession.block - 1]
		products_total = Constants.num_products[self.subsession.block - 1]
		productdims_total = Constants.productdims_total[self.subsession.block - 1]
		productdimvals_transposed = list(map(list, zip(*productdimvals)))
		preferencedims = self.session.vars["preferencedims_round" + str(self.round_number)]
		products_list = list(range(1, products_total + 1))

		best_utility = self.session.vars["productutilities_round" + str(self.round_number)][product_best - 1]

		self.player.is_mistake = is_mistake
		self.player.product_best = product_best

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
			"is_asl": self.subsession.is_asl,
			"is_mistake": is_mistake,
			"preferencedims": preferencedims,
			"productdimvals_best": productdimvals_best,
			"product_best": product_best,
			"product_selected": product_selected,
			"productdims_total": productdims_total,
			"productdimvals": productdimvals,
			"productdimvals_selected": productdimvals_selected,
			"productdimvals_transposed": productdimvals_transposed,
			"products_list": products_list,
			"products_total": products_total,
			"preferences_list": preferences_list,
			"utility_best": best_utility,
			"utilities_list": utilities_list,
			"utility_selected": selected_utility,
			"practice_round:": self.subsession.practiceround,
		}

class Splash(Page):
    form_model = models.Player
    form_fields = [ ]

# @login_required
def DataDownload(request):
	headers, body = export.export_contracts()
	return export.export_csv("Data", headers, body)

page_sequence = [
    InstructionsBasics,
    InstructionsBasicsQuiz,
    InstructionsFullInformation,
    # InstructionsTruncation,
    # InstructionsTruncationQuiz,
    # InstructionsASL,
    # InstructionsASLQuiz,
    # InstructionsNewTreatment,
    # InstructionsRoundResultsQuiz,
    PracticeBegin,
    PracticeEnd,
    ChoiceTruncation,
    ChoiceASL,
    RoundResults,
]

# page_sequence = [
#     ChoiceTruncation,
#     ChoiceASL,
#     RoundResults,
# ]