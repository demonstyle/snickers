import random
import string
import requests
import sys

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
    # Hit nike sku endpoint to get product id.
    # Sample json response:
    # {'skus': [{'id': 'a99d5708-37bf-5a05-83f6-b28d70f80b25', 'nikeSize': '10', 'countrySpecifications': [{'country': 'US', 'localizedSize': 'M 10 / W 11.5'}], 'gtin': '00193145226456', 'product': {'id': '3a4be21a-b939-597c-a1bf-19d72ab29ac0', 'brand': 'Nike', 'productType': 'FOOTWEAR', 'styleColor': 'CI2666-100', 'styleType': 'INLINE', 'pid': '12629203', 'price': {'discounted': False}, 'content': {'fullTitle': 'PG 3 NASA Basketball Shoe', 'subtitle': 'Basketball Shoe', 'colorDescription': 'White/Metallic Gold'}, 'imageSet': {'images': [{'company': 'DotCom', 'view': 'CI2666_100_A_PREM'}, {'company': 'DotCom', 'view': 'CI2666_100_B_PREM'}, {'company': 'DotCom', 'view': 'CI2666_100_C_PREM'}, {'company': 'DotCom', 'view': 'CI2666_100_D_PREM'}, {'company': 'DotCom', 'view': 'CI2666_100_E_PREM'}, {'company': 'DotCom', 'view': 'CI2666_100_F_PREM'}, {'company': 'DotCom', 'view': 'CI2666_100_N_PREM'}, {'company': 'DotCom', 'view': 'CI2666_100_O_PREM'}, {'company': 'DotCom', 'view': 'CI2666_100_P_PREM'}]}}}]}
    url = f'https://www.nike.com/checkout/services/v1/skus/{skuId}?country=us&language=en-US'
    try:
        print(f'Getting product id of {skuId}')
        r = requests.get(url)
        r.raise_for_status()
        response = r.json()
        return response['skus'][0]['product']['id']
    except requests.exceptions.HTTPError as err:
        print(err)
        sys.exit(1)

def addToCart(skuId):
    # Add sneaker to cart by sku id.
    # Sample response:
    # {"id":"a64f80fe-c84f-4bc9-9ef3-13274fc7a6d1","country":"US","currency":"USD","brand":"NIKE","channel":"NIKECOM","totals":{"subtotal":120,"discountTotal":0,"valueAddedServicesTotal":0,"total":120,"quantity":1},"items":[{"id":"3bd05e1c-863b-4485-bf11-5454337b05ab","skuId":"a99d5708-37bf-5a05-83f6-b28d70f80b25","quantity":1,"priceInfo":{"price":120,"subtotal":120,"discount":0,"valueAddedServices":0,"total":120,"priceSnapshotId":"c4509ee8-c050-4165-83f7-407677f1d9c4","msrp":120,"fullPrice":120}}],"links":{"self":{"ref":"/buy/carts/v2/US/NIKE/NIKECOM"}},"resourceType":"cart"}
    url = 'https://api.nike.com/buy/carts/v2/US/NIKE/NIKECOM?modifiers=VALIDATELIMITS,VALIDATEAVAILABILITY'
    headers = {
        'accept': 'application/json',
        'appid': 'com.nike.commerce.nikedotcom.web',
        'Content-Type': 'application/json; charset=UTF-8',
        'x-nike-visitid': '7',
        'x-nike-visitorid': '6d326d40-52a3-4557-8309-62cabe81af24'
    }
    payload = [{
        'op': 'add',
        'path': '/items',
        'value': {
            'skuId': skuId,
            'quantity': 1
        }
    }]

    try:
        r = requests.patch(url, json=payload, headers=headers)
        r.raise_for_status()
        print(f'Added {skuId} to cart')
        print(r.status_code)
        response = r.json()
        return response['items']
    except requests.exceptions.HTTPError as err:
        # print(f'Failed to add {skuId} to cart')
        print(err)
        sys.exit(1)

def removeFromCart(cartItemId):
    url = 'https://api.nike.com/buy/carts/v2/US/NIKE/NIKECOM?modifiers=VALIDATELIMITS,VALIDATEAVAILABILITY'
    headers = {
        'accept': 'application/json',
        'appid': 'com.nike.commerce.nikedotcom.web',
        'Content-Type': 'application/json; charset=UTF-8',
        'x-nike-visitid': '5',
        'x-nike-visitorid': '6d326d40-52a3-4557-8309-62cabe81af24'
    }
    payload = [{
        'op': 'remove',
        'path': '/items',
        'value': {
            'id': cartItemId
        }
    }]

    try:
        r = requests.patch(url, json=payload, headers=headers)
        r.raise_for_status()
        print(f'Deleted {cartItemId} from cart')
        print(r.status_code)
        response = r.json()
        return response['items']
    except requests.exceptions.HTTPError as err:
        # print(f'Failed to delete {cartItemId} from cart')
        print(err)
        sys.exit(1)

def setPaymentInfo(productId):
    url = 'https://api.nike.com/payment/preview/v2'
    headers = {
        'accept': 'application/json',
        'appid': 'com.nike.commerce.nikedotcom.web',
        'Content-Type': 'application/json; charset=UTF-8',
        'x-nike-visitid': '5',
        'x-nike-visitorid': '6d326d40-52a3-4557-8309-62cabe81af24'
    }
    payload = {
        'checkoutId': 'fce23e5a-f976-4f83-9ed6-f4959fe166a6',
        'total': 140.16,
        'currency': 'USD',
        'country': 'US',
        'items':[{
            'productId':productId,
            'shippingAddress':{
                'address1':'9651 Nadine Street',
                'address2':'',
                'city':'Temple City',
                'state':'CA',
                'country':'US',
                'postalCode':'91780',
                'preferred':false,
                'email':'paulyeo21@gmail.com',
                'phoneNumber':'6265905973',
                'addressId':'5f56548d-1d35-4756-842d-5b7189ff1c27'
            }
        }],
        'paymentInfo':[{
            'id':'e179ead0-e446-4715-ba7e-d38bd2b1365c',
            'creditCardInfoId':'e179ead0-e446-4715-ba7e-d38bd2b1365c',
            'type':'CreditCard',
            'cardType':'VISA',
            'lastFour':'1688',
            'expiryMonth':'10',
            'expiryYear':'2023',
            'accountNumber':'XXXXXXXXXXXX1688',
            'billingInfo':{
                'name':{
                    'firstName':'Paul',
                    'lastName':'Yeo'
                },
                'address':{
                    'address1':'9651 Nadine Street',
                    'address2':'',
                    'city':'Temple City',
                    'state':'CA',
                    'postalCode':'91780',
                    'country':'US'
                },
                'contactInfo':{
                    'phoneNumber':'6265905973',
                    'email':'paulyeo21@gmail.com'
                }
            },
            'dateOfBirth':''
        }]
    }

# sku = input('Enter sneaker SKU: ')
sku = 'a99d5708-37bf-5a05-83f6-b28d70f80b25'
# print(getProductId(sku))
cartItems = addToCart(sku)
for item in cartItems:
    removeFromCart(item['id'])

