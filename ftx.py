import requests
import json
import time

def main():
        collection = "Parallel"
        response = requests.get(
            'https://ftx.us/api/nft/nfts_filtered?startInclusive=0&endExclusive=1000000000&nft_filter_string={"collection":"' + 
            collection + '","nftAuctionFilter":"buyNow","minPriceFilter":null,"maxPriceFilter":null,"seriesFilter":[],"traitsFilter":{},"include_not_for_sale":true}&sortFunc=name_asc')
        token_id=''
        base_os_url = "https://api.opensea.io/api/v1/asset/"
        asset_contract_address = '0x76BE3b62873462d2142405439777e971754E8E77'  # Currently set to Parallel

        try:
            last_token_id=''
            for NFT in response.json()['result']['nfts']:
                # print(NFT)
                #print(NFT['ethTokenId']+" - "+NFT['name']+" - "+str(NFT['offerPrice'])+" "+NFT['quoteCurrency'])
                token_id = NFT['ethTokenId']
                ftx_price = NFT['offerPrice']

                if last_token_id != token_id:
                    last_token_id = token_id
                    try:
                        #print("sleeping")
                        #time.sleep(5)
                        os_url=base_os_url+asset_contract_address+'/'+token_id
                        response = requests.request("GET", os_url, headers={"Accept": "application/json"})
                        # print(response.json()['last_sale']['total_price'])
                        os_price = int(response.json()['last_sale']['total_price'])/1000000000000000000
                        
                        if os_price>ftx_price:
                            rake = 0.125 #10% take from parallel, 2.5% opensea
                            profit = round(os_price-ftx_price,2)
                            true_profit = round(os_price-(os_price*rake)-ftx_price,2)
                            print("ARB FOUND!")
                            print("FTX: "+NFT['name']+" - "+str(ftx_price)+" "+NFT['quoteCurrency'])
                            print("OS : "+NFT['name']+" - "+str(os_price)+" ETH")
                            print("Potential Profit:"+str(profit))
                            print("True Profit:"+str(true_profit))

                    except json.decoder.JSONDecodeError:
                        print("Can't reach opensea.")
        except json.decoder.JSONDecodeError:
            print("Can't reach ftx.")

if __name__ == "__main__":
    main()