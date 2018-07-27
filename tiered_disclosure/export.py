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
    """ return list of productdims with appropriate number of blank cells """
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

def export_contracts():
    maxprefdim = max(Constants.num_prefdims)
    maxproduct = max(Constants.num_products)
    maxproductdim = max(Constants.productdims_total)
    body = []

    # Create the header list
    session_fns, session_fns_d, group_fns, participant_fns, participant_fns_d = get_headers_simple()
    player_fns = []
    subsession_fns = ["round_number", "treatment", "practiceround", "realround", "is_asl", "num_representatives", "num_products", "num_prefdims", "productdims_total", "productdims_shown", "product_best",]
    # subsession_fns = ["round_number", "treatment", "practiceround", "realround", "num_products", "num_prefdims", "productdims_total", "productdims_shown", "product_selected", "is_mistake", "product_best"]

    player_fns_d = ["basics_q1", "product_selected", "is_mistake",]
    d = dict(enumerate(string.ascii_lowercase, 1)) #converts number to alphabet
    # prefdim_fns = ["prefdim_" + str(d[i]) for i in range(1, maxprefdim + 1)]
    # proddim_fns = ["prod_" + str(i) + "dim_" + str(d[j]) for i in range(1, maxproduct + 1) for j in range(1, maxproductdim + 1)]
    # util_fns = ["util_prod" + str(i) for i in range(1, maxproduct+1)]
    proddim_fns = ["products_round" + str(i+1) for i in range(Constants.num_rounds)]
    prefdim_fns = ["preferences_round" + str(i+1) for i in range(Constants.num_rounds)]
    util_fns = ["utilities_round" + str(i+1) for i in range(Constants.num_rounds)]
    sessions = Session.objects.order_by("code")
    for session in sessions:
        # if not session.config["name"] == "duopoly_rep_treat":
        #     continue
        session_list = list_from_obj(session_fns, session)
        proddim_list = []
        prefdim_list = []
        util_list = []
        for i in range(Constants.num_rounds):
                proddims_in_round = session.vars["productdims_round" + str(i+1)]
                proddim_list.append(proddims_in_round)
                prefdims_in_round = session.vars["preferencedims_round" + str(i+1)]
                prefdim_list.append(prefdims_in_round)
                utils_in_round = session.vars["productutilities_round" + str(i+1)]
                util_list.append(utils_in_round)
        # I believe this method excludes subsessions from other apps, and thus we do not need to filter on app name
        subsessions = Subsession.objects.filter(session=session)
        for subsession in subsessions:
            subsession_list = list_from_obj(subsession_fns, subsession)
            print("listfromobj is", list_from_obj(subsession_fns, subsession))
            # products = subsession.numproducts
            # for product in products:

            players = Player.objects.filter(subsession=subsession)
            for player in players:
                player_list = list_from_obj(player_fns_d, player)

            body.append(session_list + subsession_list + player_list + proddim_list + prefdim_list + util_list)


    headers = session_fns_d + subsession_fns + player_fns_d + proddim_fns + prefdim_fns + util_fns

    return headers, body