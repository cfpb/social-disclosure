from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import math, random, copy
import csv
import numpy as np
import pandas as pd
from otree.db.models import Model, ForeignKey

author = 'Dustin Beckett, Daniel Banko'


doc = """
Tiered Disclosure Experiment
"""

class Constants(BaseConstants):

    """
    num_prefdims: number of preference dimensions in each treatment
    num_products: number of products in each treatment
    productdims_total: number of total dimensions in each treatment
    productdims_shown: number of shown dimensions in each treatment (truncation only)
    asl_flag: whether the treatment is asl (=1) or truncation (=0)
    practicerounds: whether there should be practice rounds in each treatment
    num_rounds_treatment: number of paid rounds in each treatment
    """

    #############################################
    productdims_total = [3, 3, 3, 3]
    productdims_shown = [2, 0, 2, 0]
    num_prefdims = [3, 3, 3, 3]
    num_products = [3, 3, 6, 6]
    num_representatives = [0, 2, 0, 2]
    asl_flag = [0,1,0,1]
    practicerounds = [True, True, False, False]
    num_rounds_treatment = [2,2,1,1]
    ############################################# 

    ##############################################
    # productdims_total = [3, 3, 3, 3]
    # productdims_shown = [2, 0, 2, 0]
    # num_prefdims = [3, 3, 3, 3]
    # num_products = [3, 3, 6, 6]
    # num_representatives = [0, 2, 0, 2]
    # asl_flag = [0,1,0,1]
    # practicerounds = [True, True, False, False]
    # num_rounds_treatment = [2,2,1,1]
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
        num_rounds_practice.append(2 * int(practicerounds[i])) # two rounds of practice whenever practicerounds==1
    num_rounds = sum(num_rounds_treatment) + sum(num_rounds_practice)
    # choice_number = [x + 1 for x in range(max(num_products))]
    # choice_string = ["Product " + str(i) for i in choice_number]

    # Checking requirements
    assert(len(num_products) == len(productdims_total))
    assert(len(num_products) == len(productdims_shown))
    assert(len(num_products) == len(practicerounds))
    assert(len(num_products) == len(num_rounds_treatment))


class Subsession(BaseSubsession):
    practiceround = models.BooleanField(doc="True if subsession is a practice round")
    realround = models.BooleanField(doc="True if subsession is not a practice round")
    block = models.IntegerField(doc="The order in which the treatment was played in the session")
    block_new = models.BooleanField(default=False, doc="True if round is the first in a new treatment block")
    num_products = models.IntegerField(doc="The number of products in the treatment")
    num_representatives = models.IntegerField(doc="The number of representatives in the treatment")
    productdims_total = models.IntegerField(doc="The number of product dimensions in the treatment")
    productdims_shown = models.IntegerField(doc="The number of shown product dimensions in the treatment")
    num_prefdims = models.IntegerField(doc="The number of preference dimensions in the treatment")
    treatment = models.IntegerField(doc="The ID of the treatment ")
    is_asl = models.IntegerField(doc="1 if treatment is ASL")

    show_instructions_base = models.BooleanField(doc="True if basic instructions are to be shown this round.")
    show_instructions_block = models.BooleanField(doc="True if new-block instructions are to be shown this round.")
    show_instructions_practice = models.BooleanField(doc="True if practice round specific instructions are to be shown.")
    show_instructions_real = models.BooleanField(doc="True if real round specific instructions are to be shown.")

    bool_best_prod = models.IntegerField(doc="1 if the participant selected optimal product")
    product_best = models.IntegerField(doc="ID of product which maximizes utility for participant")
    is_mistake = models.IntegerField(doc="True if the participant selected not optimal product")
    
    productdims_round = models.IntegerField(doc="dimensions of ")

    def vars_for_admin_report(self):
        return {"session_code": self.session.code,
            }

    def before_session_starts(self):
        treatmentorder = list(map(int, self.session.config['treatmentorder'].split(',')))
        treatmentorder = [i - 1 for i in treatmentorder]
        print('treatmentorder - 1 is', treatmentorder)

        num_products = [Constants.num_products[i] for i in treatmentorder]
        productdims_total = [Constants.productdims_total[i] for i in treatmentorder]
        productdims_shown = [Constants.productdims_shown[i] for i in treatmentorder]
        print("productdims_shown = ", productdims_shown)
        num_prefdims = [Constants.num_prefdims[i] for i in treatmentorder]
        num_representatives = [Constants.num_representatives[i] for i in treatmentorder]
        asl = [Constants.asl_flag[i] for i in treatmentorder]
        practicerounds = Constants.practicerounds
        num_rounds_treatment = [Constants.num_rounds_treatment[i] for i in treatmentorder]
        num_rounds_practice = [Constants.num_rounds_practice[i] for i in treatmentorder]

        new_block_rounds = [sum(num_rounds_treatment[:i]) + sum(num_rounds_practice[:i]) + 1 for i in range(len(num_rounds_treatment) + 1)]
        print("new_block_rounds = ", new_block_rounds)
        practice_rounds = [new_block_rounds[i] + j for i in range(len(new_block_rounds) - 1) for j in range(num_rounds_practice[i])]

        #  Determine if this is the first round of a new block. This is also used to display new instructions
        if self.round_number in new_block_rounds:
            self.block_new = True
            self.block = new_block_rounds.index(self.round_number) + 1
        else:
            self.block_new = False
            # finds the block in which this round resides.
            for i in range(len(new_block_rounds)):
                if self.round_number > new_block_rounds[i] and self.round_number < new_block_rounds[i+1]:
                    self.block = i + 1
                    break
        print('round = ',self.round_number)
        self.treatment = self.block
        print("self.block = ", self.block)
        if self.round_number in practice_rounds:
            self.practiceround = True
            self.realround = False
        else:
            self.practiceround = False
            self.realround = True

        # Instructions control variables
        #   Show_instructions are instructions shown whenever a new block happens
        #   ..._roles are role specific instructions shown a subset of the time
        #   ..._practice are practice round specific instructions show a subset of the time
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
        self.representatives = num_representatives[self.block - 1]
        self.is_asl = asl[self.block - 1]
        self.num_products = num_products[self.block - 1]
        self.num_prefdims = num_prefdims[self.block - 1]
        self.num_representatives = num_representatives[self.block - 1]
        self.session.vars["productdims_round" + str(self.round_number)] = []
        self.session.vars["preferencedims_round" + str(self.round_number)] = []

        #do not delete
        #set preference profile values and utility values for each round
        # preference_dims = []
        # preferences = set_prefdims(self.preferences)["prefdims"]
        # preference_dims.append(preferences)
        # self.session.vars["preferencedims_round" + str(self.round_number)] = preferences
        # product_dims = []
        # product_utilities = []


        # csv_data = import_params_from_csv("justvals.csv")['csv_data']
        # print('productdimvals column in csv:')
        num_rounds = Constants.num_rounds
        current_round = self.round_number
        round_index = current_round - 1
        filename = "tiered_disclosure/my_data.csv"
        data = pd.read_csv(filename, quotechar='"', skipinitialspace=True).to_dict()
        products = data['productdimvals']
        preferences = data['preferencedimvals']
        representatives = data['representativedimvals']
        print('num_rounds = ', num_rounds)
        productdimvals = [data['productdimvals'][i].replace('[','').replace(']','').split(';') for i in range(num_rounds)]
        preferencedimvals = [data['preferencedimvals'][i].replace('[','').replace(']','') for i in range(num_rounds)]
        representativedimvals = [data['representativedimvals'][i].replace('[','').replace(']','') for i in range(num_rounds)]
        preference_dims = []
        preference = preferencedimvals[round_index].split(' ')
        preference_dims.append(preference)
        self.session.vars["preferencedims_round" + str(self.round_number)] = preferences
        product_dims = []
        product_utilities = []
        print(num_rounds)
        print(productdimvals)
        for i in range(self.num_products):
            product_index = i
            products_list = productdimvals[round_index]
            print(round_index)
            print(product_index)
            product = productdimvals[round_index][product_index].split(',') #YOU HAVE ROUNDS WITH MORE THAN THREE PRODUCTS SO YOU NEED TO MODIFY JUSTVALS TO FIT THOSE PRODUCTS IN!!!
            product_dims.append(product)
            # utility = calculate_utility(product, preferences)["totalutility"]
            # product_utilities.append(utility)

        self.session.vars["productdims_round" + str(self.round_number)] = product_dims
        self.session.vars["productutilities_round" + str(self.round_number)] = product_utilities
        # product_best = determine_bestproduct(product_utilities)["bestproduct"]
        # self.session.vars["bestproduct_round" + str(self.round_number)] = product_best
        print(product_dims)
        print(products_list)
        # values_dict = import_params_from_csv("justvals.csv")['csv_dict']

        # for row in values_dict:
        # self.session.vars["productdims_round" + str(self.round_number)] = csv_data['productdimvals']

        # productdimvals = group_by_field(csv_data)

        # grouped = group_by_field(csv_data)

        # print 'First closed location'
        # print grouped[''][0], '\n\n'

        # print 'Total number of closed locations'
        # print len(grouped['Closed']), '\n\n'

        # print('All productdimvals:', grouped.keys(), '\n\n')
        # product_dims = productdimvals[self.round_number]
        # self.session.vars["productdims_round" + str(self.round_number)] = product_dims

        # products = csv_data['productdimvals']
        # products_in_round = products[0]
        # product = products_in_round[0]
        # print('products')
        # print(products)
        # print(products[0])
        # print(products[0][0])
        # print('products_in_round')
        # print(products_in_round)
        # print(products_in_round[0])
        # print('product')
        # print(product)

        # test = [[0,1,2],[1,3,2],[3,2,1]]
        # test2 = test[0]
        # print(test2)
#do not delete:
        # for i in range(self.num_products):
        #     product = set_productdims(self.productdims_total)["productdims"]
        #     product_dims.append(product)
        #     utility = calculate_utility(product, preferences)["totalutility"]
        #     product_utilities.append(utility)
        # self.session.vars["productdims_round" + str(self.round_number)] = product_dims
        # self.session.vars["productutilities_round" + str(self.round_number)] = product_utilities
        # product_best = determine_bestproduct(product_utilities)["bestproduct"]
        # self.product_best = product_best

        # self.session.vars["bestproduct_round" + str(self.round_number)] = product_best

        if self.is_asl:
            representative_dims = []
            utility_reps = []
            # set representative values for asl rounds and calculate representative utility
            for i in range(self.representatives):
                current_representative = i
                representative_index = current_representative - 1
                representative_list = representativedimvals[round_index]
                # representative = set_representativedims(self.productdims_total)["representativedims"]
                representative = representativedimvals[round_index][representative_index].split(',')
                representative_dims.append(representative)
                # reputility = calculate_reputility(product_dims, representative)["representativeutility"]
                # utility_reps.append(reputility)
            self.session.vars["reputility_round" + str(self.round_number)] = utility_reps
            # self.session.vars["productdims_round" + str(self.round_number)] = representative_dims
            self.session.vars["representativedims_round" + str(self.round_number)] = representative_dims
        else:
            # set product dimension values for truncation rounds
            productdimvals_shown = []
            for j in range(1):
                truncatedvals = [0] * (self.productdims_shown)
                for i in range(1):
                    tval = -1
                    tval = product_dims[j][i]
                    truncatedvals[i] = tval
                    print(truncatedvals[i])
                    print("truncatedvals[i] is", truncatedvals[i])
                truncvalues = copy.copy(truncatedvals)
                productdimvals_shown.append(truncvalues)
            self.session.vars["productdims_shown_round" + str(self.round_number)] = productdimvals_shown
            self.productdimvals_shown = productdimvals_shown

        if self.practiceround:
            self.session.vars["practice_proddims" + str(self.round_number)] = []

        # self.productdims_round = self.session.vars["productdims_shown_round" + str(self.round_number)]

class Player(BasePlayer):
    #Instruction Questions
    basics_q1 = models.CharField(doc = "Instructions quiz, basics")
    # basics_q2 = models.CharField(doc = "Instructions quiz, basics 2")

    product_selected = models.IntegerField(doc="ID of product selected by participant")
    product_best = models.IntegerField(doc = "ID of project that is utility maximizing for participant")
    is_mistake = models.IntegerField(doc = "1 if product selected by participant was suboptimal")
    product_selected_dims = models.IntegerField(doc="dimvals of product selected by participant")

class Product(Model): #custom model inherits from Django base class "Model". Based off Ask class.
    """ Stores details of a product """
    player = ForeignKey(Player)

    # def set_productdims(self, productdims):
    #     random.seed()
    #     for i in range(self.player.subsession.dims_per_product):
    #         pd = self.productdim_set.create(dimnum=i + 1, value=random.uniform(0,1))
    #         pd.save()

def import_params_from_csv(filename):
    data = pd.read_csv(filename, quotechar='"', skipinitialspace=True).to_dict()
    products = data['productdimvals']
    # data['productdimvals'][i].replace('[','').replace(']','').split(';')
    print(products)
    print(products[0])
    print(products[1])
    # reading csv file
    # with open(filename, 'r') as csvfile:
        # creating a csv reader object
        # csvreader = csv.reader(csvfile)

        # extracting field names through first row
        # fields = next(csvreader)
    csvfile = open(filename, 'r')
    # data = np.genfromtxt(filename, delimiter=',', names=True)
    data = pd.read_csv(filename, quotechar='"', skipinitialspace=True).to_dict()
    csv_dict = csv.DictReader(csvfile) #new (I want this to be a dictionary which stores lists)
    
    for row in csv_dict:
        csv_data.append(row)
    csvfile.close()
    return {
        'csv_dict': csv_dict,
        # 'csv_data': csv_data,
        'csv_data': csv_data,
    }


def calculate_utility(productdimvals, prefdimvals):
    print('entering calculate_utility')
    print('productdimvals =', productdimvals)
    print('prefdimvals =', prefdimvals)
    total_utility = 0

    value = productdimvals
    weight = prefdimvals
    total_utility = sum([val * weigh for val, weigh in zip(value, weight)])
    print('total_utility =', total_utility)

    # for i in range(len(productdimvals) + 1):
    #     productdimval = productdimvals[i]
    #     prefdimval = prefdimvals[i]

    #     utility = productdimval*prefdimval
    #     total_utility = total_utility+utility
    return {
        'totalutility': total_utility,
    }

def calculate_reputility(productdimvals, prefdimvals):
    print('entering calculate_reputility')
    print('productdimvals =', productdimvals)
    print('prefdimvals =', prefdimvals)
    total_utility = []
    for product in productdimvals:
        value = product
        weight = prefdimvals
        product_utility = sum([val * weigh for val, weigh in zip(value, weight)])
        print('product_utility =', product_utility)
        total_utility.append(product_utility)
    return {
        'representativeutility': total_utility,
    }

def determine_bestproduct(productutilities):
    print('entering determine_bestproduct')
    product_best = -1
    max_utility= max(productutilities)
    product_best = productutilities.index(max_utility)+1
    return {
        'bestproduct': product_best, 
    }

def set_productdims(numdims):
    print('entering set_productdims')
    rawvals = [0]*numdims
    for i in range(numdims):
        val = -1
        val = random.randint(1,101)
        rawvals[i] = val

    dvalues = copy.copy(rawvals)
    print('dvalues is', dvalues)

    return {
        'productdims': dvalues,
    }

# def set_productdims_from_csv(filename, numdims):
#     print('entering set_productdims')
#     # csv file name
#     # initializing the titles and rows list
#     fields = []
#     rows = []

#     # reading csv file
#     with open(filename, 'r') as csvfile:
#         # creating a csv reader object
#         csvreader = csv.reader(csvfile)
#         fields = next(csvreader)
#         reader = csv.DictReader(csvfile, fieldnames=fields)
#         for row in reader:
#             print(row['productdims_shown'],row['productdimvals'],row['round_num'])
#         # extracting field names through first row


#         # extracting each data row one by one
#         for row in csvreader:
#             rows.append(row)

#         # get total number of rows
#         print("Total no. of rows: %d"%(csvreader.line_num))

#     # printing the field names
#     print('Field names are:' + ', '.join(field for field in fields))

#     #  printing first 5 rows
#     for row in  :
#         # parsing each column of a row
#         for col in row:
#             print("%10s"%col),
#         print('\n')

#     rawvals = [0]*numdims
#     for i in range(numdims):
#         val = -1
#         val = rows[i]
#         rawvals[i] = val

#     dvalues = copy.copy(rawvals)
#     print('dvalues is', dvalues)

#     return {
#         'productdims': dvalues,
#     }

def set_representativedims(numdims):
    print('entering set_representativedims')
    rawvals = [0]*numdims
    for i in range(numdims):
        val = -1
        val = random.randint(1,11)
        rawvals[i] = val
    rvalues = copy.copy(rawvals)
    print('rvalues is', rvalues)
    return {
        'representativedims': rvalues,
    }

def set_prefdims(preferencedims):
    print('entering set_prefprof')
    rawvals= [0]*preferencedims
    for i in range(preferencedims):
        val = -1
        val = random.randint(1,11)
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
