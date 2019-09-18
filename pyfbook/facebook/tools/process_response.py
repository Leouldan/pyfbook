import hashlib


def make_date(date_start, time_increment):
    # if time_increment == 'monthly':
    #     return datetime.datetime.strptime(date_start, '%Y-%m-%d').strftime('%Y-%m-01')
    if time_increment:
        return date_start
    print('Error time increment not specified in make_date function')
    exit()


def make_batch_id(date, account_id, campaign_id=None, adset_id=None, ad_id=None):
    for i in [campaign_id, adset_id, ad_id]:
        if not i:
            i = ""
    chi = "_".join(k for k in [str(campaign_id), str(adset_id), str(ad_id)])
    return hashlib.sha224((date + str(account_id) + str(chi)).encode()).hexdigest()