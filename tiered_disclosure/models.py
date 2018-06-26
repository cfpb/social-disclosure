from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import math, random, copy
from otree.db.models import Model, ForeignKey

author = 'Dustin Beckett, Daniel Banko'


doc = """
Tiered Disclosure Experiment
"""

class Constants(BaseConstants):

    """
    num_prefdims: number of preference dimensions in each treatment
    num_products: number of products in each treatment
    productdims_total: number of total dimensions (hidden and shown) in each treatment
    productdims_shown: number of shown dimensions in each treatment
    asl_flag: whether the treatment is asl (=1) or truncation (=0)
    practicerounds: whether there should be practice rounds in each treatment
    num_rounds_treatment: number of paid rounds in each treatment
    """

    ##############################################
    productdims_total = [3, 3]
    productdims_shown = [2, 2]
    num_prefdims = [3, 3]
    num_products = [3, 6]
    asl_flag = [0,0]
    practicerounds = [True, False]
    num_rounds_treatment = [4,4]

    ##############################################

   

    # OTHER PARAMETERS
    name_in_url = 'tiered_disclosure'
    players_per_group = None
    show_truncation_timer = False
    truncation_timer = 60
    num_treatments = len(num_products)
    show_instructions_admin = True # set false to not show any instructions

    num_rounds_practice = []
    for i in range(len(practicerounds)):
        num_rounds_practice.append(2 * int(practicerounds[i]))
        print("num_rounds_practice is", num_rounds_practice)
    num_rounds = sum(num_rounds_treatment) + sum(num_rounds_practice)
    choice_number = [x + 1 for x in range(max(num_products))]
    choice_string = ["Product " + str(i) for i in choice_number]

    # Checking requirements
    assert(len(num_products) == len(productdims_total))
    assert(len(num_products) == len(productdims_shown))
    assert(len(num_products) == len(practicerounds))
    assert(len(num_products) == len(num_rounds_treatment))


class Subsession(BaseSubsession):
    print('in creating_session')
    practiceround = models.BooleanField(doc="True if subsession is a practice round")
    realround = models.BooleanField(doc="True if subsession is not a practice round")
    block = models.IntegerField(doc="The order in which the treatment was played in the session")
    block_new = models.BooleanField(default=False, doc="True if round is the first in a new treatment block")
    num_products = models.IntegerField(doc="The number of products in the treatment")
    productdims_total = models.IntegerField(doc="The number of product dimensions in the treatment")
    productdims_shown = models.IntegerField(doc="The number of shown product dimensions in the treatment")
    num_prefdims = models.IntegerField(doc="The number of preferences in player profile in the treatment")
    treatment = models.IntegerField(doc="The ID of the treatment ")
    dim_val = models.IntegerField(doc="The values of each dimension")
    is_asl = models.IntegerField(doc="1 if treatment is ASL")

    show_instructions_base = models.BooleanField(doc="True if basic instructions are to be shown this round.")
    show_instructions_block = models.BooleanField(doc="True if new-block instructions are to be shown this round.")
    show_instructions_practice = models.BooleanField(doc="True if practice round specific instructions are to be shown.")
    show_instructions_real = models.BooleanField(doc="True if real round specific instructions are to be shown.")

    def vars_for_admin_report(self):
        return {"session_code": self.session.code,
            }

    def before_session_starts(self): #changed from before_session_starts
        treatmentorder = list(map(int, self.session.config['treatmentorder'].split(',')))
        treatmentorder = [i - 1 for i in treatmentorder]
        print('treatmentorder - 1 is', treatmentorder)

        num_products = [Constants.num_products[i] for i in treatmentorder]
        productdims_total = [Constants.productdims_total[i] for i in treatmentorder]
        productdims_shown = [Constants.productdims_shown[i] for i in treatmentorder]
        num_prefdims = [Constants.num_prefdims[i] for i in treatmentorder]
        asl = [Constants.asl_flag[i] for i in treatmentorder]
        practicerounds = Constants.practicerounds
        num_rounds_treatment = [Constants.num_rounds_treatment[i] for i in treatmentorder]
        num_rounds_practice = Constants.num_rounds_practice
        new_block_rounds = [sum(num_rounds_treatment[:i]) + sum(num_rounds_practice[:i]) + 1 for i in range(len(num_rounds_treatment) + 1)]
         # practice rounds
        practice_rounds = [new_block_rounds[i] + j for i in range(len(new_block_rounds) - 1) for j in range(num_rounds_practice[i])]


        new_block_rounds = [sum(Constants.num_rounds_treatment[:i]) + sum(Constants.num_rounds_practice[:i]) + 1 for i in range(len(num_rounds_treatment) + 1)]
        print('new_block_rounds is', new_block_rounds)
        print('round_number is', self.round_number)
        print('treatmentorder is', treatmentorder)
        print('num_products is', num_products)
        print('productdims_total is', productdims_total)
        print('productdims_shown is', productdims_shown)
        print('asl is', asl)

 		# set treatment-level variables
 		# Determine if this is the first round of a new block. This is also used to display new instructions
        if self.round_number in new_block_rounds:
            self.block_new = True
            self.block = new_block_rounds.index(self.round_number) + 1
        else:
            self.block_new = False
            # finds the block in which this round resdes.
            for i in range(len(new_block_rounds)):
                if self.round_number > new_block_rounds[i] and self.round_number < new_block_rounds[i+1]:
                    self.block = i + 1
                    break

        self.treatment = self.block

        # Is this a practice round?
        print('practice_rounds is', practice_rounds)
        print('self.round_number is', self.round_number)
        if self.round_number in practice_rounds:
            self.practiceround = True
            self.realround = False
        else:
            self.practiceround = False
            self.realround = True

        # Instructions control variables
        #   Show_instructions are instructions shown whenever a new block happens
        #   ..._roles are role specific instructions shown a subset of the time
        #   ..._practice are practice round specifc instructions show a subset of the time
        self.show_instructions_base = True if self.round_number == 1 and Constants.show_instructions_admin else False
        self.show_instructions_block = True if self.block_new and Constants.show_instructions_admin else False
        self.show_instructions_practice = True if (self.practiceround and not self.round_number-1 in practice_rounds) \
            and Constants.show_instructions_admin else False
        self.show_instructions_real = True if Constants.show_instructions_admin and (self.realround and \
            self.round_number != 1 and (self.round_number - 1 in practice_rounds or self.treatment != self.in_round(self.round_number - 1).treatment)) \
            else False
        
        # store treatment number, product dims, and number of products
        self.productdims_shown = productdims_shown[self.block - 1]
        self.productdims_total = productdims_total[self.block - 1]
        self.preferences = num_prefdims[self.block - 1]
        self.products = num_products[self.block - 1]
        self.is_asl = asl[self.block - 1]

        self.session.vars["products_round" + str(self.round_number)] = []
        product_dims = []
        for i in range(self.products):
            product_dims.append(set_productdims(self.productdims_total)["productdims"]) 
        self.session.vars["products_round" + str(self.round_number)] = product_dims

        self.session.vars["preferences_round" + str(self.round_number)] = []
        preference_dims = []
        for i in range(self.preferences):
            preference_dims.append(set_prefdims(self.preferences)["prefdims"]) 
        self.session.vars["preferences_round" + str(self.round_number)] = preference_dims
     
    #version 1 of function to not show hidden dimensions:
        productdims_shown = []
        for j in range(self.products):
            truncatedvals = [0]*(self.productdims_shown)
            for i in range(self.productdims_shown):
                tval = -1
                tval = product_dims[j][i]
                truncatedvals[i] = tval
                print("truncatedvals[i] is", truncatedvals[i])
            truncvalues = copy.copy(truncatedvals)
            productdims_shown.append(truncvalues)

        self.session.vars["products_shown_round" + str(self.round_number)] = productdims_shown

class Player(BasePlayer):
    bool_best_prod = models.IntegerField(doc="1 if the participant selected optimal product")
    best_product = models.IntegerField(doc="ID of product maximizes utility for participant")
    product_selected = models.IntegerField(doc="ID of product selected by participant")
    is_mistake = models.IntegerField(doc="True if the participant selected not optimal product")

    #TOADD: incoporate product information in product_selected using following as guide
    # contract_seller_rolenum = models.IntegerField(
    #     choices= list(zip(Constants.choice_number, Constants.choice_string)),
    #     widget=widgets.RadioSelect(),
    #     doc="If a buyer, the role number of the seller from whom the buyer purchased"
    # )
    #Instruction Questions
    basics_q1 = models.CharField(doc = "Instructions quiz, basics")

        # dim_vals = []
        # dim_val = {}
        # for i in range(1, prod_total[1]):
        #     prod_id = i
        #     for j in range(1, dims_total[1]):
        #         dim_value = random.randint(0,1)
        #         dim_id = j
        #         dim_vals.append(dim_value)
        #         dim_val["Prod"+str(prod_id)+"Dim"+str(dim_id)] = dim_value



class Product(Model): #custom model inherits from Django base class "Model". Based off Ask class.
    """ Stores details of a product """
    player = ForeignKey(Player)

    # def set_productdims(self, productdims):
    #     random.seed()
    #     for i in range(self.player.subsession.dims_per_product):
    #         pd = self.productdim_set.create(dimnum=i + 1, value=random.uniform(0,1))
    #         pd.save()


def set_productdims(numdims):
    print('entering set_productdims')
    rawvals = [0]*numdims
    for i in range(numdims):
        val = -1
        val = round(random.random(),2) #halton draws?
        rawvals[i] = val

    dvalues = copy.copy(rawvals)
    print('dvalues is', dvalues)


    return {
        'productdims': dvalues,
    }

def set_prefdims(preferencedims):
    print('entering set_prefprof')
    rawvals= [0]*preferencedims
    for i in range(preferencedims):
        val = -1
        val = round(random.random(),2)
        rawvals[i] = val

    pvalues = copy.copy(rawvals)

    print('pvalues is', pvalues)

    return {
        'prefdims': pvalues,
    }

    # for i in range(self.player.subsession.num_pref_total):
    #     pp = self.prefprof_set.create(value = round(random.random(),2)

class ProdDim(Model): #based off pricedim class

	value = models.IntegerField(doc="The value of this product dim")
	dimnum = models.IntegerField(doc="The number of the dimension of this price dim")

	product = ForeignKey(Product, blank=True, null=True)


class PrefProfile(Model):
	""" Stores details of a player profile of preferences """
	pass



class PrefDim(Model):
	value = models.IntegerField(doc="The value of this preference")
	prefID = models.IntegerField(doc="The ID of this preference")
	player = ForeignKey(Player)

class Group(BaseGroup):
    pass

