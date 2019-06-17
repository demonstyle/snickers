import random
import string
import requests
import sys

class Recipient:
    def __init__(self, fname, lname, phoneNumber, email, address1, city, state, country, postalCode):
        self.fname = fname
        self.lname = lname
        self.phoneNumber = phoneNumber
        self.email = email
        self.address1 = address1
        self.city = city
        self.state = state
        self.country = country
        self.postalCode = postalCode

class SnickersBot:
    PRODUCT_ID_KEY = 'id'
    PRODUCT_DESCRIPTION_KEY = 'fullTitle'
    COLOR_DESCRIPTION_KEY = 'colorDescription'
    STYLE_COLOR_KEY = 'styleColor'

    def __init__(self, skuId, recipient, sessionId=None):
        self.skuId = skuId
        self.productId = None
        self.productDescription = None
        self.styleColor = None
        self.colorDescription = None
        self.cartItemId = None
        self.recipient = recipient
        self.shippingId = None
        # Get product info and set as instance variables
        self.getProductInfo()
        self.headers = {
            'accept': 'application/json',
            'appid': 'com.nike.commerce.nikedotcom.web',
            'Content-Type': 'application/json; charset=UTF-8',
            'x-nike-visitid': '7',
            'x-nike-visitorid': SnickersBot.generateNikeId()
            # 'x-nike-visitorid': '6d326d40-52a3-4557-8309-62cabe81af24'
        }

    def __repr__(self):
        return f'SnickersBot# {vars(self)}'

    def getProductInfo(self):
        """Get product information by hitting nike's skus endpoint.

        Args:
            skuId (str): Shoe skuId.
        Returns:
            None
        Raises:
            requests.exceptions.HTTPError: If HTTP request returned unsuccessful status code
        """

        try:
            url = f'https://www.nike.com/checkout/services/v1/skus/{self.skuId}?country=us&language=en-US'
            r = requests.get(url)
            r.raise_for_status()
            response = r.json()
            self.productId = response['skus'][0]['product'][self.PRODUCT_ID_KEY]
            self.productDescription = response['skus'][0]['product']['content'][self.PRODUCT_DESCRIPTION_KEY]
            self.styleColor = response['skus'][0]['product'][self.STYLE_COLOR_KEY]
            self.colorDescription = response['skus'][0]['product']['content'][self.COLOR_DESCRIPTION_KEY]
        except requests.exceptions.HTTPError as err:
            print(f'Failed to get product information for {self.skuId}')
            print(err)
            sys.exit(1)

    def addToCart(self):
        """Add product to cart by given session Id and set cart item Id.

        Args:
            None
        Return:
            None
        Raises:
            requests.exceptions.HTTPError: If HTTP request returned unsuccessful status code
        """

        try:
            url = 'https://api.nike.com/buy/carts/v2/US/NIKE/NIKECOM?modifiers=VALIDATELIMITS,VALIDATEAVAILABILITY'
            payload = [{
                'op': 'add',
                'path': '/items',
                'value': {
                    'skuId': self.skuId,
                    'quantity': 1
                }
            }]
            r = requests.patch(url, json=payload, headers=self.headers)
            r.raise_for_status()
            response = r.json()
            self.cartItemId = response['items'][0]['id']
        except requests.exceptions.HTTPError as err:
            print(f'Failed to add {self.skuId} to cart')
            print(err)
            sys.exit(1)

    def removeFromCart(self):
        """Remove product from cart by given session Id and cart item Id.

        Args:
            None
        Return:
            None
        Raises:
            requests.exceptions.HTTPError: If HTTP request returned unsuccessful status code
        """

        try:
            url = 'https://api.nike.com/buy/carts/v2/US/NIKE/NIKECOM?modifiers=VALIDATELIMITS,VALIDATEAVAILABILITY'
            payload = [{
                'op': 'remove',
                'path': '/items',
                'value': {
                    'id': self.cartItemId
                }
            }]
            r = requests.patch(url, json=payload, headers=self.headers)
            r.raise_for_status()
            self.cartItemId = None
        except requests.exceptions.HTTPError as err:
            print(f'Failed to remove {self.cartItemId} from cart')
            print(err)
            sys.exit(1)

    def setShippingInfo(self):
        try:
            url = 'https://api.nike.com/buy/cart_reviews/v1/'
            self.shippingId = SnickersBot.generateNikeId()
            payload = {
                'resourceType':'buy/cart_reviews',
                'country':'US',
                'currency':'USD',
                'brand':'NIKE',
                'channel':'NIKECOM',
                'items':[{
                    'id': self.shippingId,
                    'skuId': self.skuId,
                    'shippingAddress':{
                        'address1': recipient.address1,
                        'city': recipient.city,
                        'state': recipient.state,
                        'postalCode': recipient.postalCode,
                        'country': recipient.country,
                        'email': recipient.email,
                        'phoneNumber': recipient.phoneNumber,
                        'firstName': recipient.fname,
                        'lastName': recipient.lname
                    },
                    'recipient':{
                        'firstName': recipient.fname,
                        'lastName': recipient.lname
                    },
                    'shippingMethod':{'id':'STANDARD'},
                    'quantity':1,
                    'contactInfo':{
                        'phoneNumber': recipient.phoneNumber,
                        'email': recipient.email
                    }
                }],
                'promotionCodes':[]
            }
            r = requests.post(url, json=payload, headers=self.headers)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(f'Failed to set shipping information')
            print(err)
            sys.exit(1)

    def setPaymentInfo(self):
        url = 'https://api.nike.com/payment/preview/v2'
        payload = {
            'checkoutId': 'fce23e5a-f976-4f83-9ed6-f4959fe166a6',
            'total': 140.16,
            'currency': 'USD',
            'country': 'US',
            'items':[{
                'productId': self.productId,
                'shippingAddress':{
                    'address1': recipient.address1,
                    'address2':'',
                    'city': recipient.city,
                    'state': recipient.state,
                    'country': recipient.country,
                    'postalCode': recipient.postalCode,
                    'preferred':false,
                    'email': recipient.email,
                    'phoneNumber': recipient.phoneNumber,
                    'addressId': self.shippingId
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

    def getCartInfo(self):
        try:
            url = 'https://api.nike.com/buy/carts/v2/US/NIKE/NIKECOM'
            r = requests.get(url, headers=self.headers)
            r.raise_for_status()
            return r.json()
        except requests.exceptions.HTTPError as err:
            print(f'Failed to get cart information')
            print(err)
            sys.exit(1)

    def login(self):
        try:
            url = 'https://unite.nike.com/login'
            payload = {
                'username': 'paulyeo21@gmail.com',
                'password': 'Pauly3ok',
                'ux_id': 'com.nike.commerce.nikedotcom.web',
                'grant_type': 'password'
            }
            r = requests.post(url, headers=self.headers)
            r.raise_for_status()
            return r.json()
        except requests.exceptions.HTTPError as err:
            print(f'Failed to get cart information')
            print(err)
            sys.exit(1)


    @staticmethod
    def generateNikeId():
        """Generate a random Id for nike requests that matches the following regex:
        ^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$

        Args:
            None

        Returns:
            str: Random alphanumeric Id, i.e. c287c8b3-bd5f-4341-959c-d9121997662c.
        """

        return SnickersBot.generateAlphanumeric(8) + '-' \
                + SnickersBot.generateAlphanumeric(4) + '-' \
                + SnickersBot.generateAlphanumeric(4) + '-' \
                + SnickersBot.generateAlphanumeric(4) + '-' \
                + SnickersBot.generateAlphanumeric(12)

    @staticmethod
    def generateAlphanumeric(length):
        """Generate a random alphanumeric [0-9a-fA-F] string of given length.

        Args:
            length (int): The length of return string.

        Returns:
            str: Random alphanumeric string.
        """

        return ''.join(random.choices('0123456789abcdefABCDEF', k=length))

if __name__ == '__main__':
    # sku = input('Enter sneaker SKU: ')
    me = Recipient('paul', 'yeo', '6265905973', 'paulyeo21@gmail.com', \
            '9651 Nadine Street', 'Temple City', 'CA', 'USA', '91780')
    skuId = 'a99d5708-37bf-5a05-83f6-b28d70f80b25'
    bot = SnickersBot(skuId, me)
    bot.login()
    # print(bot.getCartInfo())
    # bot.addToCart()
    # bot.removeFromCart()
    # print(bot)
    # print(SnickersBot.generateNikeId())

