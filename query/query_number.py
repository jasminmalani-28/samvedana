from query.query import *


def number_selection(land_account, distribution_option, startdate, enddate):
    dist_num = ''
    selection_list = []

    if not land_account:
        number = '0'
    else:
        if land_account == 'All':
            number = '1'
        else:
            number = '2'

    if distribution_option == 'ration':
        dist_num = '1'
    elif distribution_option == 'tadpatri':
        dist_num = '2'
    elif distribution_option == 'SewingMachine':
        dist_num = '3'
    elif distribution_option == 'All':
        dist_num = '4'

    if not startdate:
        date_num = '1'
    else:
        if not enddate:
            date_num = '1'
        else:
            date_num = '2'

    selection_list.append(number)
    selection_list.append(dist_num)
    selection_list.append(date_num)

    return selection_list


def query_selection(land_number, distribution_number, date_number, land_accountNumber, startdate, enddate):
    ration = ''
    tadpatri = ''
    sewingMachine = ''

    query_list = []

    if land_number == '2':
        if distribution_number == '1' and date_number == '1':
            ration = spc_ration(land_accountNumber)
        elif distribution_number == '1' and date_number == '2':
            ration = date_with_spc_ration(land_accountNumber, startdate, enddate)
        elif distribution_number == '2' and date_number == '1':
            tadpatri = spc_tadpatri(land_accountNumber)
        elif distribution_number == '2' and date_number == '2':
            tadpatri = date_with_spc_tadpatri(land_accountNumber, startdate, enddate)
        elif distribution_number == '3' and date_number == '1':
            sewingMachine = spc_sewingMachine(land_accountNumber)
        elif distribution_number == '3' and date_number == '2':
            sewingMachine = date_with_spc_sewingMachine(land_accountNumber, startdate, enddate)
        elif distribution_number == '4' and date_number == '1':
            ration = spc_ration(land_accountNumber)
            sewingMachine = spc_sewingMachine(land_accountNumber)
            tadpatri = spc_tadpatri(land_accountNumber)
        elif distribution_number == '4' and date_number == '2':
            ration = date_with_spc_ration(land_accountNumber, startdate, enddate)
            tadpatri = date_with_spc_tadpatri(land_accountNumber, startdate, enddate)
            sewingMachine = date_with_spc_sewingMachine(land_accountNumber,startdate, enddate)
    elif land_number == '1' or land_number == '0':
        if distribution_number == '1' and date_number == '1':
            ration = ration_all()
        elif distribution_number == '1' and date_number == '2':
            ration  = date_ration(startdate, enddate)
        elif distribution_number == '2' and date_number == '1':
            tadpatri = tadpatri_all()
        elif distribution_number == '2' and date_number == '2':
            tadpatri = date_tadpatri(startdate, enddate)
        elif distribution_number == '3' and date_number == '1':
            sewingMachine = sewingMachine_all()
        elif distribution_number == '3' and date_number == '2':
            sewingMachine = date_sewingMachine(startdate, enddate)
        elif distribution_number == '4' and date_number == '1':
            ration = ration_all()
            sewingMachine = sewingMachine_all()
            tadpatri = tadpatri_all()
        elif distribution_number == '4' and date_number == '2':
            ration = date_ration(startdate, enddate)
            tadpatri = date_tadpatri(startdate, enddate)
            sewingMachine = date_sewingMachine(startdate, enddate)

    query_list.append(ration)
    query_list.append(tadpatri)
    query_list.append(sewingMachine)

    return query_list

