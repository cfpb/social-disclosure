from .models import Constants, Subsession, Player, Group
# from survey.models import Subsession as SubsessionSurvey
# from survey.models import Player as PlayerSurvey
from otree.models.session import Session
from otree.models.participant import Participant

from . import models
from otree.export import get_field_names_for_csv, inspect_field_names
from django.http import HttpResponse
import datetime
import csv
import inspect
import six
import string
# from otree.common_internal import get_models_module, app_name_format
from collections import OrderedDict
from statistics import pstdev
import collections


# HELPER METHODS
def export_csv(title, headers, body):
    # filename = get_filename("marketdata")
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{} (accessed {}).csv"'.format(title,
        datetime.date.today().isoformat()
    )

    writer = csv.writer(response)
    writer.writerow(headers)
    writer.writerows(body)

    return response

def list_from_obj(fieldnames, obj):
    """
        Small helper function to create a list from an object <obj> using <fieldnames>
        as attributes.
    """

    data = []
    for f in fieldnames:
        if type(obj) == dict:
            data.append(obj[f])
        else:
            data.append("" if getattr(obj, f)==None else getattr(obj, f))

    return data


def get_headers_simple():
    session_fns = ['code', 'id']
    session_fns_display = ['session_' + fn for fn in session_fns]
    group_fns = ['id_in_subsession']
    # group_fns_display = ['group_id']
    participant_fns = ['code', 'label', 'id_in_session']
    participant_fns_display = ['participant_' + fn for fn in participant_fns]

    # return session_fns, session_fns_display, group_fns, group_fns_display, participant_fns, participant_fns_display
    return session_fns, session_fns_display, group_fns, participant_fns, participant_fns_display


def get_product_list(productdims, productdims_total, maxproductdim):
    """ return list of pricedims with appropriate number of blank cells """
    if len(productdims) == 0:
        # only here if this row is not yet populated (checking data mid-stream)
        productdim_list = [""] * maxproddim
    else:
        productdim_list = []
        for i in range(1, maxproductdim + 1):
            if i <= productdims_total:
                productdim_list += [productdims[i - 1].value]
            else:
                productdim_list += [""]

    return productdim_list

def get_pd_list_bot(pricedims, dims, maxprefdim):
    """ return list of pricedims with appropriate number of blank cells for a bot used in practice round"""
    if len(pricedims) == 0:
        # only here if this row is not yet populated (checking data mid-stream)
        pricedim_list = [""] * maxprefdim
    else:
        pricedim_list = []
        for i in range(1, maxprefdim + 1):
            if i <= dims:
                pricedim_list += [pricedims[i - 1]]
            else:
                pricedim_list += [""]

    return pricedim_list

# EXPORT FUNCTIONS
# def export_asks():
#     """
#         Sends headers and data to views for csv data viewing/export.
#         Much code taken from:
#             https://github.com/WZBSocialScienceCenter/otree_custom_models/blob/master/example_decisions/views.py
#     """
#     maxprefdim = max(Constants.treatmentdims)
#     body = []
#     session_fns, session_fns_d, group_fns, group_fns_d, participant_fns, participant_fns_d = get_headers_simple()

#     # Create the header list
#     subsession_fns = ['round_number', 'practiceround', 'treatment']
#     player_fns = ['id_in_group', 'rolenum']
#     ask_fns = ['total', 'stdev', 'auto', 'manual']

#     headers = session_fns_d + subsession_fns + group_fns_d + participant_fns_d + player_fns + ask_fns
#     for i in range(1, maxprefdim + 1):
#         headers.append("p" + str(i))

#     # get all sessions, order them by label
#     sessions = Session.objects.order_by("code")
#     # loop through all sessions
#     print(sessions)
#     for session in sessions:
#         print("session")
#         if not session.config["name"] == "general_dimension":
#             continue
#         session_list = list_from_obj(session_fns, session)

#         print(session_list)
#         # loop through all subsessions (i.e. rounds) ordered by round number
#         subsessions = sorted(models.Subsession.objects.filter(session=session, dims__gt = 1),
#                              key=lambda x: x.round_number)
#         print(subsessions)
#         for subsession in subsessions:
#             print("subsession")
#             subsession_list = list_from_obj(subsession_fns, subsession)

#             # loop through all groups ordered by ID
#             groups = sorted(subsession.get_groups(), key=lambda x: x.id_in_subsession)
#             for group in groups:
#                 group_list = list_from_obj(group_fns, group)

#                 # loop through all players ordered by ID
#                 players = sorted(models.Player.objects.filter(group=group, roledesc="Seller"),
#                                  key=lambda x: x.participant.id_in_session)
#                 for player in players:
#                     participant = player.participant
#                     player_list = list_from_obj(participant_fns, participant) + list_from_obj(player_fns, player)

#                     asks=sorted(models.Ask.objects.filter(player=player), key=lambda x: x.id)
#                     for ask in asks:
#                         ask_list = list_from_obj(ask_fns, ask)
#                         print(ask_list)
#                         print(ask)

#                         pds = sorted(ask.pricedim_set.all(), key=lambda x: x.dimnum)
#                         pd_list = get_pd_list(pds, subsession.dims, maxprefdim)

#                         body.append( session_list + subsession_list + group_list + player_list + ask_list + pd_list )

#     return headers, body


def export_contracts():

    maxprefdim = max(Constants.num_prefdims)
    maxproduct = max(Constants.num_products)
    maxproductdim = max(Constants.productdims_total)

    print('maxprefdim is', maxprefdim)

    body = []

    # Create the header list
    session_fns, session_fns_d, group_fns, participant_fns, participant_fns_d = get_headers_simple()
    player_fns = []
    subsession_fns = ["round_number", "treatment", "practiceround", "realround", "num_products", "num_prefdims", "productdims_total", "productdims_shown"]
    player_fns_d = ["product_selected", "is_mistake", "best_product", "time_seconds"]
    d = dict(enumerate(string.ascii_lowercase, 1))
    prefdim_fns = ["prefdim_" + str(d[i]) for i in range(1, maxprefdim + 1)]
    proddim_fns = ["prod_" + str(i) + "dim_" + str(d[j]) for i in range(1, maxproduct + 1) for j in range(1, maxproductdim + 1)]
    playerutil_fns = ["util_prod" + str(i) for i in range(1, maxproduct+1)]
    sessions = Session.objects.order_by("code")
    for session in sessions:
        # if not session.config["name"] == "duopoly_rep_treat":
        #     continue
        session_list = list_from_obj(session_fns, session)

        # I believe this method excludes subsessions from other apps, and thus we do not need to filter on app name
        subsessions = Subsession.objects.filter(session=session)
        for subsession in subsessions:
            subsession_list = list_from_obj(subsession_fns, subsession)

            # products = subsession.numproducts
            # for product in products:

            proddim_list = session.vars["products_round" + "1"]
            prefdim_list = session.vars["preferences_round" + "2"]
            print("proddim_list is", proddim_list)
            print("prefdim_list is", prefdim_list) 
            # groups = subsession.get_groups()
            # for group in groups:
            #     group_list = list_from_obj(group_fns, group)

            #     contracts = group.contract_set.all()
            #     for contract in contracts:
            #         seller = contract.ask.player
            #         buyer = contract.bid.player

            #         player_list = [seller.participant.code, seller.id_in_group, buyer.participant.code,
            #                        buyer.id_in_group]

            #         contract_list = [contract.ask.total, contract.ask.stdev]

            #         pd_list = get_pd_list(seller.get_pricedims(), subsession.dims, maxprefdim)

                    # body.append(session_list + subsession_list + group_list + player_list + contract_list + pd_list)
            body.append(session_list + subsession_list + proddim_list + prefdim_list)

    headers = session_fns_d + subsession_fns + player_fns_d + prefdim_fns + proddim_fns

    return headers, body


# def export_surveydata():
#     """

#         :return:
#     """
#     body=[]

#     subsession_fns = []
#     player_fns = []
#     session_fns, session_fns_d, group_fns, group_fns_d, participant_fns, participant_fns_d = get_headers_simple()

#     sessions = Session.objects.order_by("code")
#     for session in sessions:
#         # if not session.config["name"] == "duopoly_rep_treat":
#         #     continue
#         session_list = list_from_obj(session_fns, session)

#         subsessions = [ss for ss in session.get_subsessions() if ss.__class__._meta.app_config.name=="survey"]
#         for subsession in subsessions:
#             # print(subsession._meta.app_config.name)
#             subsession_fns = subsession_fns or get_field_names_for_csv(subsession.__class__)
#             subsession_list = list_from_obj(subsession_fns, subsession)

#             players = sorted(subsession.get_players(), key=lambda x: x.participant.id_in_session)
#             for player in players:
#                 player_fns = player_fns or get_field_names_for_csv(player.__class__)
#                 participant = player.participant

#                 player_list = list_from_obj(participant_fns, participant) + list_from_obj(player_fns, player)

#                 body.append(session_list + subsession_list + player_list)

#     headers = session_fns_d + subsession_fns + participant_fns_d + player_fns

#     return headers, body

# def get_market_headers(maxprefdim):
#     """ Helper function to create headers """
#     hdrs = []
#     seller_names = ["S" + str(rolenum + 1) for rolenum in range(max(Constants.num_sellers))]
#     for role in seller_names: 
#         for suffix in ["participant_id_in_session", "participant_code", "payoff", "ask_total", "ask_stdev", "numsold"]:
#             hdrs.append(role + "_" + suffix)
#         for i in range(1, maxprefdim + 1):
#             hdrs.append(role + "_p" + str(i))

#     buyer_names = ["B" + str(rolenum + 1) for rolenum in range(max(Constants.num_buyers))]
#     for role in buyer_names:
#         for suffix in ["participant_id_in_session", "participant_code", "payoff", "bid_total","contract_seller_rolenum"]:
#             hdrs.append(role + "_" + suffix)

#     return hdrs

# def get_market_row(group, dims, maxprefdim):
#     """ Helper function to create market-level data """
#     market_list = []
#     seller_names = ["S" + str(rolenum + 1) for rolenum in range(max(Constants.num_sellers))]
#     buyer_names = ["B" + str(rolenum + 1) for rolenum in range(max(Constants.num_buyers))]

#     if group.subsession.practiceround:
#         player = group.get_player_by_id(1)
#         asks = player.participant.vars["practice_asks" + str(group.subsession.round_number)]
#         bids = player.participant.vars["practice_bids" + str(group.subsession.round_number)]
#         numsold = list(map(sum, zip(*bids)))
#         if player.roledesc == "Seller":
#             market_list += [player.participant.id_in_session, player.participant.code, player.payoff,
#                             player.ask_total, player.ask_stdev, player.numsold]
#             market_list += get_pd_list(player.get_pricedims(), dims, maxprefdim)

#             # SELLER IN PRACTICE ROUND
#             for i in range(1, max(Constants.num_sellers)):
#                 try:
#                     market_list += [0, "bot", 0, sum(asks[i]), pstdev(asks[i]), numsold[i]]
#                     market_list += get_pd_list_bot(asks[i], dims, maxprefdim)
#                 except (ValueError, IndexError):
#                     market_list += ([""] * 6) + ([""] * max(Constants.treatmentdims))
#             # BUYER IN PRACTICE ROUND
#             for i in range(max(Constants.num_buyers)):
#                 try:
#                     market_list += [0, "bot", 0, sum(asks[bids[i].index(1)]), bids[i].index(1)]
#                 except (ValueError, IndexError):
#                     market_list += ([""] * 5)

#         else:
#             # SELLER IN PRACTICE ROUND
#             for i in range(max(Constants.num_sellers)):
#                 try:
#                     market_list += [0, "bot", 0, sum(asks[i]), pstdev(asks[i]), numsold[i]]
#                     market_list += get_pd_list_bot(asks[i], dims, maxprefdim)
#                 except (ValueError, IndexError):
#                    market_list += ([""] * 6) + ([""] * max(Constants.treatmentdims))
#             market_list += [player.participant.id_in_session, player.participant.code, player.payoff,
#                             player.bid_total, player.contract_seller_rolenum]

#             # BUYER IN PRACTICE ROUND
#             for i in range(1, max(Constants.num_buyers)):
#                 try:
#                     market_list += [0, "bot", 0, sum(asks[bids[i].index(1)]), bids[i].index(1)]
#                 except (ValueError, IndexError):
#                     market_list += ([""] * 5)

#     else:
#         # SELLER IN REAL ROUND
#         for role in seller_names: 
#             try:
#                 seller = group.get_player_by_role(role)
#                 market_list += [seller.participant.id_in_session, seller.participant.code, seller.payoff,
#                                 seller.ask_total, seller.ask_stdev, seller.numsold]
#                             # add price dims and appropriate number of blank spaces
#                 market_list += get_pd_list(seller.get_pricedims(), dims, maxprefdim)
#             except ValueError:
#                 market_list += ([""] * 6) + ([""] * max(Constants.treatmentdims))

#         # BUYER IN REAL ROUND
#         for role in buyer_names:
#             try:
#                 buyer = group.get_player_by_role(role)
#                 market_list += [buyer.participant.id_in_session, buyer.participant.code, 
#                                 buyer.payoff, buyer.bid_total, buyer.contract_seller_rolenum]
#             except ValueError:
#                 market_list += ([""] * 5)
#     return market_list

# def export_marketdata():
#     """

#         :return:
#     """

#     maxprefdim = max(Constants.treatmentdims)
#     body = []
#     session_fns, session_fns_d, group_fns, group_fns_d, participant_fns, participant_fns_d = get_headers_simple()

#     subsession_fns = ["round_number", "realround", "treatment"]
#     group_fns = get_field_names_for_csv(Group)
#     market_fns = get_market_headers(maxprefdim)

#     headers = session_fns_d + subsession_fns + group_fns + market_fns

#     sessions = Session.objects.order_by("code")
#     for session in sessions:
#     #     if not session.config["name"] == "duopoly_rep_treat":
#     #         continue
#         session_list = list_from_obj(session_fns, session)

#         # I believe this method excludes subsessions from other apps, and thus we do not need to filter on app name
#         subsessions = Subsession.objects.filter(session=session)
#         for subsession in subsessions:
#             subsession_list = list_from_obj(subsession_fns, subsession)

#             groups = subsession.get_groups()
#             for group in groups:

#                 group_list = list_from_obj(group_fns, group)
#                 market_list = get_market_row(group, subsession.dims, maxprefdim)

#                 # players = sorted(group.get_players(), key=lambda x: x.participant.id_in_session)
#                 # for player in players:
#                 #     player_fns = player_fns or get_field_names_for_csv(player.__class__)

#                 body.append(session_list + subsession_list + group_list + market_list)

#     return headers, body


# def export_combineddata():
#     """
#         Getting ALL the fields in one place
#         This will not return all Asks (only latest)
#         This will not return response times
#         This will not return payment data
#         :return: csv headers and body for output
#     """
#     maxprefdim = max(Constants.treatmentdims)
#     body = []
#     # only using the participant headers from this ...
#     session_fns, session_fns_d, group_fns, group_fns_d, participant_fns, participant_fns_d = get_headers_simple()

#     session_fns = ["id"] + get_field_names_for_csv(Session)
#     metadata_fns = ["date", "time"]
#     subsession_fns = get_field_names_for_csv(Subsession) # this will only get the market subsessions (not survey)
#     group_fns = get_field_names_for_csv(Group)
#     market_fns = get_market_headers(maxprefdim)
#     player_fns = get_field_names_for_csv(Player)
#     pricedim_fns = ["p" + str(i) for i in range(1, maxprefdim + 1)]
#     survey_fns = get_field_names_for_csv(PlayerSurvey)
#     survey_fns = [ fn for fn in survey_fns if not fn in ["payoff", "id_in_group"] ]

#     headers = session_fns + metadata_fns + subsession_fns + group_fns + market_fns + participant_fns_d + player_fns + \
#               pricedim_fns + survey_fns

#     sessions = Session.objects.order_by("pk")
#     # subsessions = [ss for ss in session.get_subsessions() if ss.__class__._meta.app_config.name == "survey"]

#     for session in sessions:
#         # if not session.config["name"] == "duopoly_rep_treat":
#         #     continue
#         session_list = list_from_obj(session_fns, session)
#         metadata_list = list_from_obj(metadata_fns, session.config)

#         # I believe this method excludes subsessions from other apps, and thus we do not need to filter on app name
#         subsessions = Subsession.objects.filter(session=session)
#         for subsession in subsessions:
#             subsession_list = list_from_obj(subsession_fns, subsession)

#             groups = subsession.get_groups()
#             for group in groups:
#                 group_list = list_from_obj(group_fns, group)
#                 market_list = get_market_row(group, subsession.dims, maxprefdim)

#                 players = group.get_players()
#                 for player in players:
#                     participant = player.participant
#                     participant_list = list_from_obj(participant_fns, participant)
#                     player_list = list_from_obj(player_fns, player)
#                     pricedim_list = get_pd_list(player.get_pricedims(), subsession.dims, maxprefdim)

#                     player_survey = PlayerSurvey.objects.get(session=session, participant__code=participant.code)
#                     survey_list = list_from_obj(survey_fns, player_survey)


#                     body.append(session_list + metadata_list + subsession_list + group_list + market_list +
#                                 participant_list + player_list + pricedim_list + survey_list)

#     return headers, body


# def export_docs(app_name):
#     """
#         Taken and adapted from the otree core: https://github.com/oTree-org/otree-core/blob/master/otree/export.py
#         Adapting to export to csv and to add non-standard models
#     """

#     # generate doct_dict
#     models_module = get_models_module(app_name)

#     model_names = ["Participant", "Player", "Group", "Subsession", "Session", "Ask", "Bid", "Contract", "PriceDim"]
#     line_break = '\r\n'

#     def choices_readable(choices):
#         lines = []
#         for value, name in choices:
#             # unicode() call is for lazy translation strings
#             lines.append(u'{}: {}'.format(value, six.text_type(name)))
#         return lines

#     def generate_doc_dict():
#         doc_dict = OrderedDict()

#         data_types_readable = {
#             'PositiveIntegerField': 'positive integer',
#             'IntegerField': 'integer',
#             'BooleanField': 'boolean',
#             'CharField': 'text',
#             'TextField': 'text',
#             'FloatField': 'decimal',
#             'DecimalField': 'decimal',
#             'CurrencyField': 'currency'}

#         for model_name in model_names:
#             if model_name == 'Participant':
#                 Model = Participant
#             elif model_name == 'Session':
#                 Model = Session
#             else:
#                 Model = getattr(models_module, model_name)
#             # print(model_name)

#             field_names = set(field.name for field in Model._meta.fields)

#             members = get_field_names_for_csv(Model)
#             if not members:
#                 members = [f for f in inspect_field_names(Model)]
#             doc_dict[model_name] = OrderedDict()

#             for member_name in members:
#                 member = getattr(Model, member_name, None)
#                 doc_dict[model_name][member_name] = OrderedDict()
#                 if member_name == 'id':
#                     doc_dict[model_name][member_name]['type'] = ['positive integer']
#                     doc_dict[model_name][member_name]['doc'] = ['Unique ID']
#                 elif member_name in field_names:
#                     member = Model._meta.get_field_by_name(member_name)[0]

#                     internal_type = member.get_internal_type()
#                     data_type = data_types_readable.get(internal_type, internal_type)

#                     doc_dict[model_name][member_name]['type'] = [data_type]

#                     # flag error if the model doesn't have a doc attribute,
#                     # which it should unless the field is a 3rd party field
#                     doc = getattr(member, 'doc', '[error]') or ''
#                     doc_dict[model_name][member_name]['doc'] = [
#                         line.strip() for line in doc.splitlines() if line.strip()]

#                     choices = getattr(member, 'choices', None)
#                     if choices:
#                         doc_dict[model_name][member_name]['choices'] = (choices_readable(choices))
#                 elif isinstance(member, collections.Callable):
#                     doc_dict[model_name][member_name]['doc'] = [inspect.getdoc(member)]
#         return doc_dict

#     def docs_as_lists(doc_dict):
#         header = ["Model", "Field", "Type", "Description"]
#         body = [['{}: Documentation'.format(app_name_format(app_name))], ['*' * 15],
#                 ['Accessed: {}'.format(datetime.date.today().isoformat())], ['']]

#         app_doc = getattr(models_module, 'doc', '')
#         if app_doc:
#             body += [app_doc, '']

#         for model_name in doc_dict:
#             for member in doc_dict[model_name]:
#                 # lines.append('\t{}'.format(member))
#                 for info_type in doc_dict[model_name][member]:
#                     # lines.append('\t\t{}'.format(info_type))
#                     for info_line in doc_dict[model_name][member][info_type]:
#                         # lines.append(u'{}{}'.format('\t' * 3, info_line))
#                         body += [[model_name, member, info_type, info_line]]

#         return header, body

#     doc_dict = generate_doc_dict()
#     return docs_as_lists(doc_dict)