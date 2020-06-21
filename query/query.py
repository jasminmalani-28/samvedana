ration = """select DISTINCT beneficiary_detail.land_accountnumber,beneficiary_detail.beneficiary_name,
                   beneficiary_detail.village_name,ration_details.date,ration_details.type,ration_details.quantity 
                   from samvedana.beneficiary_detail,samvedana.ration_details 
                   where beneficiary_detail.land_accountnumber=ration_details.land_accountnumber"""

tadpatri = """select DISTINCT beneficiary_detail.land_accountnumber,beneficiary_detail.beneficiary_name,
                        beneficiary_detail.village_name,tadpatri_details.date,tadpatri_details.type,
                        tadpatri_details.quantity from samvedana.beneficiary_detail,samvedana.tadpatri_details
                        where beneficiary_detail.land_accountnumber=tadpatri_details.land_accountnumber"""

sewingMachine = """select DISTINCT beneficiary_detail.land_accountnumber,
                        beneficiary_detail.beneficiary_name, beneficiary_detail.village_name,sewingmachine_detail.date,
                        sewingmachine_detail.type, sewingmachine_detail.quantity from samvedana.beneficiary_detail,
                        samvedana.sewingmachine_detail where 
                        beneficiary_detail.land_accountnumber=sewingmachine_detail.land_accountnumber"""


def ration_all():
    return ration


def tadpatri_all():
    return tadpatri


def sewingMachine_all():
   return sewingMachine


def spc_ration(accountNumber):
    ration_query = ration + ' and ration_details.land_accountnumber = "{}" '.format(accountNumber)
    return ration_query


def spc_tadpatri(accountNumber):
    tadpatri_query = tadpatri + ' and tadpatri_details.land_accountnumber = "{}" '.format(accountNumber)
    return tadpatri_query


def spc_sewingMachine(accountNumber):
    sewingMachine_query = sewingMachine + ' and sewingmachine_detail.land_accountnumber = "{}" '.format(accountNumber)
    return sewingMachine_query


def date_ration(startdate, enddate):
    ration_query = ration + ' and ration_details.date BETWEEN "{}" and "{}" '.format(startdate, enddate)
    return ration_query


def date_tadpatri(startdate, enddate):
    tadpatri_query = tadpatri + ' and tadpatri_details.date BETWEEN "{}" and "{}" '.format(startdate, enddate)
    return tadpatri_query


def date_sewingMachine(startdate, enddate):
    sewingMachine_query = sewingMachine + ' and sewingmachine_detail.date BETWEEN "{}" and "{}" '.format(startdate, enddate)
    return sewingMachine_query


def date_with_spc_ration(accountnumber, startdate, enddate):
    ration_query = spc_ration(accountnumber) + ' and ration_details.date BETWEEN "{}" and "{}" '.format(startdate, enddate)
    return ration_query


def date_with_spc_tadpatri(accountnumber, startdate, enddate):
    tadpatri_query = spc_tadpatri(accountnumber) + ' and tadpatri_details.date BETWEEN "{}" and "{}" '.format(startdate, enddate)
    return tadpatri_query


def date_with_spc_sewingMachine(accountnumber, startdate, enddate):
    sewingMachine_query = spc_sewingMachine(accountnumber) + ' and sewingmachine_detail.date BETWEEN "{}" and "{}" '.format(startdate, enddate)
    return sewingMachine_query