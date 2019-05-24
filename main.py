import random, string
import requests

def generateId():
    # Generate random id for nike requests that match regex:
    # ^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$
    # i.e. c287c8b3-bd5f-4341-959c-d9121997662c
    return generateAlphanumeric(8) + '-' \
            + generateAlphanumeric(4) + '-' \
            + generateAlphanumeric(4) + '-' \
            + generateAlphanumeric(4) + '-' \
            + generateAlphanumeric(12)

def generateAlphanumeric(length):
    return ''.join(random.choices('0123456789abcdefABCDEF', k=length))

def getProductId(skuId):
    # {'skus': [{'id': 'a99d5708-37bf-5a05-83f6-b28d70f80b25', 'nikeSize': '10', 'countrySpecifications': [{'country': 'US', 'localizedSize': 'M 10 / W 11.5'}], 'gtin': '00193145226456', 'product': {'id': '3a4be21a-b939-597c-a1bf-19d72ab29ac0', 'brand': 'Nike', 'productType': 'FOOTWEAR', 'styleColor': 'CI2666-100', 'styleType': 'INLINE', 'pid': '12629203', 'price': {'discounted': False}, 'content': {'fullTitle': 'PG 3 NASA Basketball Shoe', 'subtitle': 'Basketball Shoe', 'colorDescription': 'White/Metallic Gold'}, 'imageSet': {'images': [{'company': 'DotCom', 'view': 'CI2666_100_A_PREM'}, {'company': 'DotCom', 'view': 'CI2666_100_B_PREM'}, {'company': 'DotCom', 'view': 'CI2666_100_C_PREM'}, {'company': 'DotCom', 'view': 'CI2666_100_D_PREM'}, {'company': 'DotCom', 'view': 'CI2666_100_E_PREM'}, {'company': 'DotCom', 'view': 'CI2666_100_F_PREM'}, {'company': 'DotCom', 'view': 'CI2666_100_N_PREM'}, {'company': 'DotCom', 'view': 'CI2666_100_O_PREM'}, {'company': 'DotCom', 'view': 'CI2666_100_P_PREM'}]}}}]}
    url = f'https://www.nike.com/checkout/services/v1/skus/{skuId}?country=us&language=en-US'
    r = requests.get(url)
    response = r.json()
    return response['skus'][0]['product']['id']

# print(generateId())
print(getProductId('a99d5708-37bf-5a05-83f6-b28d70f80b25'))
