import requests
import json
import urllib

OS_MAPPING = {
    'Blitmap': 'blitmap',
    'Bored%20Ape%20Kennel%20Club': 'bored-ape-kennel-club',
    'Bored%20Ape%20Yacht%20Club': 'boredapeyachtclub',
    'Capsule%20House': 'capsulehouse',
    'Creature%20World': 'creatureworld',
    'CrypToadz%20by%20GREMPLIN': 'cryptoadz-by-gremplin',
    'CryptoKitties': 'cryptokitties',
    'CryptoPunks': 'cryptopunks',
    'DeadFellaz': 'deadfellaz',
    'Depictives': 'depictives',
    'Doodles': 'doodles-official',
    'Forgotten%20Runes%20Wizards%20Cult': 'forgottenruneswizardscult',
    'Little%20Lemon%20Friends': 'little-lemon-friends',
    'loomlocknft%20%28Wassies%29': 'loomlock',
    'Meebits': 'meebits',
    'Mutant%20Ape%20Yacht%20Club': 'mutant-ape-yacht-club',
    'OnChain%20Monkey': 'onchainmonkey',
    'Parallel': 'parallelalpha',
    'Parallel%20Alpha': 'parallelalpha',
    'Pudgy%20Penguins': 'pudgypenguins',
    'Somnium%20Space%20VR': 'somnium-space',
    'The%20Doge%20Pound': 'the-doge-pound',
    'the%20littles%20NFT': 'thelittlesnft',
    'Wonky%20Stonks': 'wonky-stonks',
    'World%20of%20Women': 'world-of-women-nft'
}


def get_contract_address(uri_safe_name):
    contract_base_url = 'https://ftx.us/api/nft/example_nft?collection='
    nft = requests.get(contract_base_url + uri_safe_name)
    # print(nft.json()['result']['ethContractAddress'])
    contract_address = nft.json()['result']['ethContractAddress']
    return contract_address


def main():
    header = {
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Accept": "application/json",
        "X-API-KEY": ""
    }
    collection_names = requests.get(
        'https://ftx.us/api/nft/collection_names?startInclusive=0&endExclusive=50&collectionType=eth')
    collection_names = collection_names.json()['result']['collections']
    # collection_test = requests.get('https://ftx.us/api/nft/collection/Bored%20Ape%20Yacht%20Club')
    collection_base_url = 'https://ftx.us/api/nft/collection/'

    for collection_name in collection_names:
        # print(collection_name)
        collection_name = urllib.parse.quote(collection_name)
        collection = requests.get(collection_base_url+collection_name)
        ftx_floor = collection.json()['result']['floor_price']
        floor_currency = collection.json()['result']['floor_price_currency']

        if ftx_floor:
            # print(ftx_floor)
            # print(collection_name+' - '+str(ftx_floor)+' '+floor_currency)
            contract_address = get_contract_address(collection_name)
            rake = requests.get('https://api.opensea.io/api/v1/asset_contract/' +
                                contract_address,headers=header).json()['opensea_seller_fee_basis_points']
            rake = rake*0.0001
            if collection_name in OS_MAPPING:
                os_collection = requests.get(
                    'https://api.opensea.io/api/v1/collection/'+OS_MAPPING[collection_name]+'/stats',headers=header)
                os_floor = os_collection.json()['stats']['floor_price']
                # print(os_floor)
                if os_floor and ftx_floor < os_floor:
                    diff = round(os_floor-ftx_floor, 2)
                    print("--------------------YATZEE--------------------")
                    print(collection_name+' '+str(diff))
                    print("----------------------------------------------")
            else:
                print("Missing dictionary entry:"+collection_name)


if __name__ == "__main__":
    main()
