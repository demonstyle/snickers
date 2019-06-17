/**
 * Bot class
**/

const request = require('request');

class SnickersApi {
  static addToCart(skuId, visitorId) {
    const options = {
      url: 'https://api.nike.com/buy/carts/v2/US/NIKE/NIKECOM?modifiers=VALIDATELIMITS,VALIDATEAVAILABILITY',
      method: 'PATCH',
      headers: {
        'accept': 'application/json',
        'appid': 'com.nike.commerce.nikedotcom.web',
        'Content-Type': 'application/json; charset=UTF-8',
        'x-nike-visitid': '1',
        'x-nike-visitorid': visitorId
      },
      json: [{
        'op': 'add',
        'path': '/items',
        'value': {
          'skuId': skuId,
          'quantity': 1
        }
      }]
    }

    request(options, function(err, res, body) {
      if (err) {
        console.log(err);
      }
      // console.log(body);
    });
    // self.cartItemId = response['items'][0]['id']
  }

  static generateNikeId() {
    return this.generateAlphanumeric(8) + '-'
            + this.generateAlphanumeric(4) + '-'
            + this.generateAlphanumeric(4) + '-'
            + this.generateAlphanumeric(4) + '-'
            + this.generateAlphanumeric(12)
  }

  static generateAlphanumeric(length) {
    let result = '';
    const chars = 'abcdef0123456789';
    for (let i = 0; i < length; i++) {
      result += chars.charAt(Math.floor(Math.random() * chars.length))
    }
    return result;
  }
}

module.exports = SnickersApi;
