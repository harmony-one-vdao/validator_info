from requests import get, post
from json import dump
from datetime import datetime

block_number = 10000000
harmony_api = "https://g.s0.t.hmny.io"


def rpc_v2(result: list, method: str, params: list) -> dict:
    d = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1,
    }
    try:
        r = post(harmony_api, json=d)
        data = r.json()["result"]
    except KeyError:
        print(r)
    result += data
    return result, data


def time_of_block(block_number: int) -> str:
    res, harmony_data = rpc_v2([], "eth_getBlockByNumber", [block_number, True])
    ts = int(harmony_data["timestamp"], 16)
    date_ts = datetime.fromtimestamp(ts)
    return date_ts, date_ts.strftime("%d-%m-%y")


def months_between_dates(date_from: datetime) -> int:
    today = datetime.today()
    return (today.year - date_from.year) * 12 + today.month - date_from.month


created_dt, created_str = time_of_block(block_number)
print(created_str)
months = months_between_dates(created_dt)
print(months)
