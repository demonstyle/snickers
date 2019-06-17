/**
 * Inputs: skuId, nike account, payment information, and shipping 
 * information.
**/

const puppeteer = require('puppeteer');
const { performance } = require('perf_hooks');
const SnickersApi = require('./SnickersApi');

const skuId = 'ae4ed43f-3230-55f1-a2fa-f9120ad06cd4';
const visitorId = SnickersApi.generateNikeId();
const cookie = {
  name: 'visitData',
  value: `{"visit":"1","visitor":"${visitorId}"}`,
  domain: 'unite.nike.com',
  path: '/',
  httpOnly: false,
  secure: false,
  sameSite: 'no_restriction'
};

console.log(visitorId);

try {
  (async () => {
    const v0 = performance.now();

    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    // 1. Add shoe to cart
    SnickersApi.addToCart(skuId, visitorId);

    // 2. Navigate to page with cookie data
    await page.setCookie(cookie),
    await page.goto('https://www.nike.com/checkout', {
      waitUntil: 'networkidle2'
    });

    // 3. Get checkoutId in sessionStorage
    const checkoutId = await page.evaluate(() => {
      return sessionStorage.getItem('checkoutId');
    });
    console.log(checkoutId);

    await browser.close();
    console.log('total milliseconds: ' + (performance.now() - v0));
  })();
} catch (err) {
  console.log(err);
}
