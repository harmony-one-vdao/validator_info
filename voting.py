from core.util import *
from core.smartstake_connect import find_smartstakeid

# check a single wallets vote
check_wallet = 'one199wuwepjjefwyyx8tc3g74mljmnnfulnzf7a6a'

def get_validator_voting_info(
    fn: str, num_pages: int = 10, save_json_data: bool = False
) -> None:
    voted, voted_results = call_api(vote_full_address)
    voted_yes_weight = 0
    voted_no_weight = 0
    binance_kucoin = 0
    binance_controlled_stake = 0

    csv_data = []
    result = []
    grouped_data = {
        "email": [],
        "twitter": [],
        "website": [],
        "telegram": [],
        "at_only": [],
        "unknown": [],
    }

    for i in range(0, num_pages):
        d = {
            "jsonrpc": "2.0",
            "method": "hmy_getAllValidatorInformation",
            "params": [i],
            "id": 1,
        }
        data = post(harmony_api, json=d).json()["result"]

        if not data:
            print(f"NO MORE DATA.. ENDING ON PAGE {i+1}.")
            break

        result += data

        for d in data:
            include = False

            v, e = create_named_tuple_from_dict(d)

            eth_add = convert_one_to_hex(v.address)

            show = False
            if v.address == check_wallet:
                show = True

            if v.name in ("Binance Staking", "KuCoin"):
                binance_kucoin += e.total_delegation
                if v.name == 'Binance Staking':
                    binance_controlled_stake += e.total_delegation

            for d in v.delegations:
                if d["delegator-address"] == binance_wallet:
                    binance_controlled_stake += d["amount"]


            if e.active_status == "active":
                w = [v.name, v.address, v.security_contact, v.website, e.epos_status, e.active_status]
                grouped, app = parse_contact_info(v) 

                if eth_add not in voted:
                    include = True
                    grouped_data[app] += grouped
                    w.append(app)

                # Already Voted, Check Weight
                else:
                    choice = voted_results[eth_add]["msg"]["payload"]["choice"]
                    if int(choice) == 1:
                        voted_yes_weight += e.total_delegation
                        if show:
                            display_check = f'\n\tWallet *- {check_wallet} -* Voted Yes!\n'
                    else:
                        voted_no_weight += e.total_delegation
                        if show:
                            display_check = f'\n\tWallet *- {check_wallet} -* Voted NO!'

                if w[0] not in [x[0] for x in csv_data] and include:
                    hPoolId = find_smartstakeid(v.address, smartstake_validator_list)
                    w += [
                        smartstake_address_summary.format(hPoolId),
                        smartstake_address_blskeys.format(hPoolId),
                    ]
                    csv_data.append(w)

    save_csv(
        f"{vote_name}-{fn}",
        csv_data, 
        [
            "Name",
            "Address",
            "Security Contact",
            "Website",
            "Epos Status",
            "Active Status",
            "Group",
            "Smartstake Summary",
            "Smartstake BlsKeys",
        ],
    )

    display_stats = voted_no_weight, voted_yes_weight, binance_kucoin, binance_controlled_stake, display_check
    save_and_display(f"{vote_name}-", result, grouped_data, display_stats, display_vote_stats, save_json_data=save_json_data)


if __name__ == "__main__":
    get_validator_voting_info(
        vote_fn, num_pages=10, save_json_data=True
    )

    # l = call_api()
    # print(l)

    # sort_group('@ColorReader on Telegram.')
