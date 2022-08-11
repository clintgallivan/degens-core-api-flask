
# * Run once a day to update token timestamp - call get_token_timestamp_and_post_concurrently(token_id_list)

from operator import index
import requests
import pandas as pd
import numpy as np
import time
import random
import json
# from datetime import date
# import datetime as dt
# import pytz
coingecko_base_url = 'https://api.coingecko.com/api/v3'
mongo_base_url = 'http://127.0.0.1:5000'


def get_token_current_metadata():
    r = requests.get(f'{mongo_base_url}/tokens', timeout=600)
    return r.json()


def reduce_timeseries_data(table):
    # * create a new table with all the tokens
    df1 = pd.DataFrame(sort_by_score(table, 'coingecko_score'))
    df2 = pd.DataFrame(sort_by_score(table, 'dev_score'))
    df3 = pd.DataFrame(sort_by_score(table, 'community_score'))
    df4 = pd.DataFrame(sort_by_score(table, 'liquidity_score'))
    df5 = df1.merge(df2, how="left", on=["coingecko_id", "symbol", "name", "image"]).merge(
        df3, how="left", on=["coingecko_id", "symbol", "name", "image"]).merge(df4, how="left", on=["coingecko_id", "symbol", "name", "image"])
    df_deg = df5.sort_values(by="coingecko_score_rank")
    df_dev = df5.sort_values(by="dev_score_rank")
    df_comm = df5.sort_values(by="community_score_rank")
    df_liq = df5.sort_values(by="liquidity_score_rank")

    print('beginning table reduction')

    ds1 = {
        "by_degen_score": list(df_deg.transpose().to_dict().values())[0:100],
        "by_developer_score": list(df_dev.transpose().to_dict().values())[0:100],
        "by_community_score": list(df_comm.transpose().to_dict().values())[0:100],
        "by_liquidity_score": list(df_liq.transpose().to_dict().values())[0:100]
    }
    return json.dumps(ds1)


def data_reducer(table):
    # ds_combined
    ds_deg = []
    ds_dev = []
    ds_comm = []
    ds_liq = []
    print('beginning timeseries data reduction')
    degen_score_list = sort_by_score(table, 'coingecko_score')
    dev_score_list = sort_by_score(table, 'dev_score')
    community_score_list = sort_by_score(table, 'community_score')
    liquidity_score_list = sort_by_score(table, 'liquidity_score')
    for idx, i in enumerate(degen_score_list):
        ds_deg.append(
            {"coingecko_id": i["coingecko_id"], "degen_rank": idx + 1})
    for idx, i in enumerate(dev_score_list):
        ds_dev.append({"coingecko_id": i["coingecko_id"], "dev_rank": idx + 1})
    for idx, i in enumerate(community_score_list):
        ds_comm.append(
            {"coingecko_id": i["coingecko_id"], "community_rank": idx + 1})
    for idx, i in enumerate(liquidity_score_list):
        ds_liq.append(
            {"coingecko_id": i["coingecko_id"], "liquidity_rank": idx + 1})
    df1 = pd.DataFrame(ds_deg)
    df2 = pd.DataFrame(ds_dev)
    df3 = pd.DataFrame(ds_comm)
    df4 = pd.DataFrame(ds_liq)
    df5 = df1.merge(df2, how="left", on="coingecko_id").merge(
        df3, how="left", on="coingecko_id").merge(df4, how="left", on="coingecko_id")
    ds = list(df5.transpose().to_dict().values())
    # print(json.dumps(ds))
    return json.dumps(ds)


def sort_by_score(table, sort_column='coingecko_score', thresholds=[50, 100, 250, 500, 750, 1000]):
    sorted_table_by_mcap = sorted(
        table, key=lambda k: k['market_cap_rank'] or 0, reverse=False)
    rank = 1
    # df = pd.DataFrame(sorted_table_by_mcap, columns=[
    #                   'coingecko_id', 'market_cap_rank'])
    # print(df)
    sorted_table_by_sort_column = sorted(
        sorted_table_by_mcap, key=lambda k: k[sort_column] or 0, reverse=True)
    c1 = []
    c2 = []
    c3 = []
    c4 = []
    c5 = []
    c6 = []
    c7 = []
    c8 = []
    c9 = []
    c10 = []
    c11 = []
    c12 = []
    c13 = []
    c14 = []
    for token in sorted_table_by_sort_column:
        new_token_obj = {
            "coingecko_id": token["coingecko_id"],
            "name": token["name"],
            "symbol": token["symbol"],
            "score": token[sort_column],
            f"{sort_column}": token[sort_column],
            "image": token["image"]

        }
        if not token['market_cap_rank'] and token[sort_column] <= 0:
            c14.append(new_token_obj)
        elif not token['market_cap_rank'] and token[sort_column] > 0:
            c12.append(new_token_obj)
        elif token['market_cap_rank'] <= thresholds[0] and token[sort_column] > 0:
            c1.append(new_token_obj)
        elif token['market_cap_rank'] <= thresholds[1] and token[sort_column] > 0:
            c3.append(new_token_obj)
        elif token['market_cap_rank'] <= thresholds[2] and token[sort_column] > 0:
            c4.append(new_token_obj)
        elif token['market_cap_rank'] <= thresholds[3] and token[sort_column] > 0:
            c6.append(new_token_obj)
        elif token['market_cap_rank'] <= thresholds[4] and token[sort_column] > 0:
            c8.append(new_token_obj)
        elif token['market_cap_rank'] <= thresholds[5] and token[sort_column] > 0:
            c9.append(new_token_obj)
        elif token['market_cap_rank'] > thresholds[5] and token[sort_column] > 0:
            c12.append(new_token_obj)
        elif token['market_cap_rank'] <= thresholds[0] and token[sort_column] <= 0:
            c2.append(new_token_obj)
        elif token['market_cap_rank'] <= thresholds[1] and token[sort_column] <= 0:
            c5.append(new_token_obj)
        elif token['market_cap_rank'] <= thresholds[2] and token[sort_column] <= 0:
            c7.append(new_token_obj)
        elif token['market_cap_rank'] <= thresholds[3] and token[sort_column] <= 0:
            c10.append(new_token_obj)
        elif token['market_cap_rank'] <= thresholds[4] and token[sort_column] <= 0:
            c11.append(new_token_obj)
        elif token['market_cap_rank'] <= thresholds[5] and token[sort_column] <= 0:
            c13.append(new_token_obj)
        elif token['market_cap_rank'] > thresholds[5] and token[sort_column] <= 0:
            c14.append(new_token_obj)
    # print(len(c1))
    output = c1 + c2 + c3 + c4 + c5 + c6 + c7 + c8 + c9 + c10 + c11 + c12 + c13
    outputsm = c1 + c2
    final_output = []
    rank = 1
    for i in output:
        # print(i)
        new_item = {
            "coingecko_id": i["coingecko_id"],
            "name": i["name"],
            "symbol": i["symbol"],
            f"{sort_column}": i[sort_column],
            f"{sort_column}_rank": rank,
            "image": i["image"]
        }
        rank = rank + 1
        final_output.append(new_item)
    # print(newItem)

    # return output
    return final_output

    # df1 = pd.DataFrame(output, columns=[
    #     'coingecko_id', 'market_capd


def post_to_snapshot_db(ds):
    headers = {'Content-type': 'application/json'}
    r = requests.post(f'{mongo_base_url}/token-top-snapshot',
                      data=ds, headers=headers)
    print(r)


def post_to_update_timeseries_db(ds):
    print('begin post')
    headers = {'Content-type': 'application/json'}
    requests.post(f'{mongo_base_url}/token-timeseries',
                  data=ds, headers=headers)
    # print(r)
    print('finished_posting_timeseries')


def post_to_update_metadata_db(ds):
    print('begin post')
    headers = {'Content-type': 'application/json'}
    requests.post(f'{mongo_base_url}/update-token',
                  data=ds, headers=headers)
    print('finished_posting_metadata')


def get_top_token_snapshot_and_post_concurrently():
    print('beginning parse through token list')
    table = get_token_current_metadata()
    print('posting to db')
    post_to_snapshot_db(reduce_timeseries_data(table))
    post_to_update_timeseries_db(data_reducer(table))
    post_to_update_metadata_db(data_reducer(table))
    print('done')


# * Run once a day to insert top token document - call get_token_timestamp_and_post_concurrently(token_id_list)
