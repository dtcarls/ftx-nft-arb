import requests
import json

def main():
    collections = ["Parallel","Parallel Alpha"]
    for collection in collections:
        #collection = "Parallel Alpha"
        response = requests.get(
            'https://ftx.us/api/nft/nfts_filtered?startInclusive=0&endExclusive=1000000000&nft_filter_string={"collection":"' + 
            collection + '","nftAuctionFilter":"buyNow","minPriceFilter":null,"maxPriceFilter":null,"seriesFilter":[],"traitsFilter":{},"include_not_for_sale":true}&sortFunc=name_asc')
        token_id=''
        base_os_url = "https://api.opensea.io/api/v1/asset/"
        asset_contract_address = '0x76BE3b62873462d2142405439777e971754E8E77'  # Currently set to Parallel

        try:
            last_token_id=''
            for NFT in response.json()['result']['nfts']:

                #print(NFT['ethTokenId']+" - "+NFT['name']+" - "+str(NFT['offerPrice'])+" "+NFT['quoteCurrency'])
                token_id = NFT['ethTokenId']
                ftx_price = NFT['offerPrice']

                if last_token_id != token_id:
                    last_token_id = token_id
                    try:
                        os_url=base_os_url+asset_contract_address+'/'+token_id
                        response = requests.request("GET", os_url, headers={"Accept": "application/json"})
                        # print(response.json()['last_sale']['total_price'])
                        rake = int(response.json()['orders'][0]['taker_relayer_fee'])/10000
                        last_os_price = int(response.json()['last_sale']['total_price'])/1000000000000000000

                        orders = response.json()['orders']
                        #side 0 = offer
                        #side 1 = listing
                        largest_offer = 0
                        for order in orders:
                            if order['side'] == 0:
                                offer = (int(order['current_bounty'])/int(order['quantity']))/10000000000000000
                                if offer>largest_offer:
                                    largest_offer=offer
                        
                        if last_os_price>ftx_price:
                            profit = round(last_os_price-ftx_price,2)
                            true_profit = round(last_os_price-(last_os_price*rake)-ftx_price,2)
                            print("ARB FOUND!")
                            print("FTX: "+NFT['name']+" - "+str(ftx_price)+" "+NFT['quoteCurrency'])
                            print("OS : "+NFT['name']+" - "+str(last_os_price)+" ETH")
                            print("Potential Profit:"+str(profit))
                            print("Profit after rake:"+str(true_profit))
                        
                        if largest_offer>ftx_price:
                            profit = round(largest_offer-ftx_price,2)
                            true_profit = round(largest_offer-(largest_offer*rake)-ftx_price,2)
                            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX ARB FOUND! XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                            print("FTX: "+NFT['name']+" - "+str(ftx_price)+" "+NFT['quoteCurrency'])
                            print("OS : "+NFT['name']+" - "+str(largest_offer)+" ETH")
                            print("Potential Profit:"+str(profit))
                            print("Profit after rake:"+str(true_profit))

                    except json.decoder.JSONDecodeError:
                        print("Can't reach opensea.")
        except json.decoder.JSONDecodeError:
            print("Can't reach ftx.")

if __name__ == "__main__":
    main()