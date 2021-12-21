# ftx-nft-arb
# FTX NFT - Monitor

## Installation :

    pip install -r requirements.txt

## Configuration :

**Edit : _config.json_**

Exemple :

```
{
    "collections": [
        {
            "collection": "<collection>",
            "price": 1,
            "webhooks": [
                {
                    "name": "<name>",
                    "url": "<url>",
                    "footer_name": "<footer_name>",
                    "footer_image_url": "<footer_image_url>"
                },
                {
                    "name": "<name>",
                    "url": "<url>",
                    "footer_name": "<footer_name>",
                    "footer_image_url": "<footer_image_url>"
                }
            ]
        },
        {
            "collection": "<collection>",
            "price": 1,
            "webhooks": [
                {
                    "name": "<name>",
                    "url": "<url>",
                    "footer_name": "<footer_name>",
                    "footer_image_url": "<footer_image_url>"
                },
                {
                    "name": "<name>",
                    "url": "<url>",
                    "footer_name": "<footer_name>",
                    "footer_image_url": "<footer_image_url>"
                }
            ]
        }
    ],
    "avatar_url": "https://pbs.twimg.com/profile_images/1420493756726272002/S0sQq2-t_400x400.png"
}
```

You can find collection name at the end of : https://ftx.us/nfts/collection/Solstead

#### Warning !

At the end of the last "}" or "]" do not put a ","

Exemple :

```
{
    "collections": [
        {
            "collection": "<collection>",
            "price": 1,
            "webhooks": [
                {
                    "name": "<name>",
                    "url": "<url>",
                    "footer_name": "<footer_name>",
                    "footer_image_url": "<footer_image_url>"
                } !!!
            ]
        } !!!
    ],
    "avatar_url": "https://pbs.twimg.com/profile_images/1420493756726272002/S0sQq2-t_400x400.png"
}
```

## Execution :

    python ftx.py