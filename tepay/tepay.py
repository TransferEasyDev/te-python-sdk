# -*- coding: utf-8 -*-
# @Time : 2022/5/20下午13:14
# @Author : anwen
# @Email : anwen@transfereasy.com
# @FileName : tepay.py
# @Software: PyCharm

""" TE跨境支付通道 """

import time
import requests
import json
import rsa
from urllib.parse import quote_plus
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as pk115
from Crypto.Hash import SHA256
from base64 import b64encode
from exception.facade_exceptions import FacadeException
from tools.logger import logger
from domain.entities.money import Money


class TEPay:
    def __init__(self, product_code, mchid, channel_mchid,
                 pub_path, pri_path, facade_config, debug=True):

        self._debug = debug
        self._gateway = 'https://api.transfereasy.com' if not self._debug else 'https://test-newapi.transfereasy.com'
        self._app_notify_url = facade_config
        self._productcode = product_code
        self._mchid = mchid
        self._channel_mchid = channel_mchid
        self._publickey_path = pub_path
        self._privatekey_path = pri_path
        self._publickey = None
        self._privatekey = None

        logger.info(
            f"""
        Facade.tepay.tepay.pay
            构造TEPay对象：
            self._gateway = {self._gateway}
            self._publickey_path = {self._publickey_path}
            self._privatekey_path = {self._privatekey_path}
            """
        )

    @property
    def publickey(self):
        if not self._publickey:
            with open(self._publickey_path, 'r') as f:
                self._publickey = f.read()

        return RSA.importKey(self._publickey)

    @property
    def privatekey(self):
        if not self._privatekey:
            with open(self._privatekey_path, 'r') as f:
                self._privatekey = f.read()

        return RSA.importKey(self._privatekey)

    def _request(self, url, data, headers, timeout=20, method='POST'):

        """ 发起HTTP请求 """

        logger.info(
            f"""
        facade.TEPay._request:
            method: {method}
            url: {url}
            data: {data}
            headers: {headers}
            timeout: {timeout}
            """
        )

        if method == 'POST':
            response = requests.post(
                url,
                json=data,
                headers=headers,
                timeout=timeout
            )
        else:
            message = f'tepay._request does not support {method}'
            logger.info(
                f"""
            facade.TEPay._response:
                method: {method}
                url: {url}
                data: {data}
                headers: {headers}
                timeout: {timeout}
                error: {message}
                """
            )
            # raise FacadeException(
            #     message=message
            # )
            raise ValueError(message)

        logger.info(
            f"""
        facade.TEPay._response:
            method: {method}
            url: {url}
            data: {data}
            headers: {headers}
            timeout: {timeout}
            response: {response.content}
            """
        )
        return response

    def _build_request_headers(self, ts, sign):

        mchid = self._mchid
        channel_mchid = self._channel_mchid

        return {
            'Content-Type': 'application/json',
            'MerchantNO': mchid,
            # 'ChildMerchantNo': channel_mchid,
            'ProductCode': self._productcode,
            'Timestamp': ts,
            'Signature': sign
        }

    def _sign(self, data):

        time_stamp = str(int(time.time()))
        signature_str = "&".join((
            "=".join((k, quote_plus(str(v)) if not isinstance(v, list)
                      else quote_plus(
                          json.dumps(
                              v,
                              separators=(',', ':'),
                              sort_keys=True,
                              ensure_ascii=False
                          )
                      ))) for k, v in sorted(data.items())
        ))
        signature_str += ',' + time_stamp

        logger.info(
            f"""
        facade.tepay.tepay 签名：
            ts: {time_stamp}
            sign_str: {signature_str}
            """
        )

        cipher = pk115.new(self.privatekey)
        hash_obj = SHA256.new(signature_str.encode('utf-8'))
        signature = b64encode(
            cipher.sign(hash_obj)
        ).decode('utf-8')

        logger.info(
            f"""
        facade.tepay.tepay 签名：
            ts: {time_stamp}
            sign_str: {signature_str}
            signature: {signature}
            """
        )

        return time_stamp, signature

    def consult_payment(self, **kwargs):

        """ 查询钱包列表 """

        url = f'{self._gateway}/V1/transaction/consultPayment'

        tradeType = kwargs.get('tradeType')

        data = {
            'amount': kwargs.get('amount'),
            'currency': kwargs.get('currency'),
            'settleCurrency': kwargs.get('settleCurrency'),
            'tradeType': tradeType,
            'presentmentMode': kwargs.get('presentmentMode'),
        }
        if tradeType != 'WEB':
            data.setdefault('osType', 'IOS')

        ts, sign = self._sign(data)
        headers = self._build_request_headers(
            ts,
            sign
        )

        response = self._request(
            url,
            data,
            headers
        )

        r = json.loads(response.content)

        if r.get('code') != 1000:
            raise FacadeException(
                message=r.get('msg')
            )

        return r

    def search_rate(self, **kwargs):

        """ 人民币参考汇率查询 """

        url = f'{self._gateway}/V1/transaction/searchRate'

        data = {
            'feeType': kwargs.get('feeType'),
            'date': kwargs.get('date'),
        }

        ts, sign = self._sign(data)
        headers = self._build_request_headers(
            ts,
            sign
        )

        response = self._request(
            url,
            data,
            headers
        )

        r = json.loads(response.content)

        if r.get('code') != 1000:
            raise FacadeException(
                message=r.get('msg')
            )

        return r

    def payment(self, **kwargs):

        """ 支付 """

        url = f'{self._gateway}/V1/transaction/payment'

        trade_type = kwargs.get('tradeType')
        subject = kwargs.get('subject') or \
                  f'tepay subject of {kwargs.get("outTradeNo")}'
        return_url = kwargs.get('return_url')
        # 跨境 = ALIPAY_CN 本地 = ALIPAY_HK
        wallet_brand = 'ALIPAY_HK' if \
            kwargs.get('walletBrand') == 'ALIPAYHK' else 'ALIPAY_CN'

        data = {
            'outTradeNo': kwargs.get('outTradeNo'),
            'amount': kwargs.get('amount'),
            'currency': kwargs.get('currency'),
            'settleCurrency': kwargs.get('settleCurrency'),
            'tradeType': trade_type,
            'productInfo': [
                {
                    'name': subject,
                    'quantity': 1,
                    'amount': kwargs.get('amount'),
                    'description': subject
                }
            ],
            'clientIp': kwargs.get('clientIp'),
            'notifyUrl': self._app_notify_url.replace('alipay', 'tepay'),
            'walletBrand': wallet_brand,
            'remark': subject,
        }
        if trade_type != 'WEB':
            data.setdefault('osType', 'IOS')
        if return_url:
            data.setdefault('returnUrl', return_url)

        ts, sign = self._sign(data)
        headers = self._build_request_headers(
            ts,
            sign
        )

        response = self._request(
            url,
            data,
            headers
        )

        r = json.loads(response.content)

        if r.get('code') != 1000:
            raise FacadeException(
                message=r.get('msg')
            )

        return r

    def query_payment(self, **kwargs):

        """ 支付单查询 """

        url = f'{self._gateway}/V1/transaction/searchPayment'

        out_trade_no = kwargs.get('payment_no')

        data = {
            'outTradeNo': out_trade_no,
        }
        ts, sign = self._sign(data)
        headers = self._build_request_headers(
            ts,
            sign
        )

        response = self._request(
            url,
            data,
            headers
        )

        r = json.loads(response.content)

        if r.get('code') != 1000:
            raise FacadeException(
                message=r.get('msg')
            )

        return r

    def close_payment(self, **kwargs):

        """ 支付单取消 """

        url = f'{self._gateway}/V1/transaction/closePayment'

        out_trade_no = kwargs.get('payment_no')

        data = {
            'outTradeNo': out_trade_no,
        }
        ts, sign = self._sign(data)
        headers = self._build_request_headers(
            ts,
            sign
        )

        response = self._request(
            url,
            data,
            headers
        )

        r = json.loads(response.content)

        if r.get('code') != 1000:
            raise FacadeException(
                message=r.get('msg')
            )

        return r

    def refund(self, **kwargs):

        """ 退款 """

        url = f'{self._gateway}/V1/transaction/refund'

        data = {
            'outTradeNo': kwargs.get('outTradeNo'),
            'paymentNo': kwargs.get('paymentNo'),
            'refundAmount': kwargs.get('refundAmount'),
            'remark': f'Proxy refund of payment: {kwargs.get("paymentNo")}'
        }

        ts, sign = self._sign(data)
        headers = self._build_request_headers(
            ts,
            sign
        )

        response = self._request(
            url,
            data,
            headers
        )

        r = json.loads(response.content)

        if r.get('code') != 1000:
            raise FacadeException(
                message=r.get('msg')
            )

        return r

    def refund_query(self, **kwargs):

        """ 退款查询 """

        url = f'{self._gateway}/V1/transaction/searchRefund'

        data = {
            'outTradeNo': kwargs.get('outTradeNo'),
        }
        ts, sign = self._sign(data)
        headers = self._build_request_headers(
            ts,
            sign
        )

        response = self._request(
            url,
            data,
            headers
        )
        r = json.loads(response.content)

        if r.get('code') != 1000:
            raise FacadeException(
                message=r.get('msg')
            )

        return r

    def download_bill(self, **kwargs):

        """ 导出对账单 """

        url = f'{self._gateway}/bill/download'

        data = {
            'billDate': kwargs.get('billDate'),
            'currency': kwargs.get('currency')
        }
        ts, sign = self._sign(data)
        headers = self._build_request_headers(
            ts,
            sign
        )

        reponse = self._request(
            url,
            data,
            headers
        )

    def alipay_declaration(self, **kwargs):

        """ 报关/重推 """

        url = f'{self._gateway}/V1/customs/declare'
        # url = f'{self._gateway}/V1/customs/redeclare'     # 重推

        data = {
            'outTradeNo': kwargs.get('outTradeNo'),
            'paymentNo': kwargs.get('paymentNo'),
            'customs': kwargs.get('customs'),
            'merchantCustomsCode': kwargs.get('merchantCustomsCode'),
            'merchantCustomsName': kwargs.get('merchantCustomsName'),
            'isSplit': kwargs.get('isSplit'),
        }
        if son := kwargs.get('subOrderNo'):
            data['isSplit'] = 'true'
            data.setdefault('subOrderNo', son)
            sub_order_money = Money(
                currency='CNY',
                amount=kwargs.get('subOrderAmount')
            )
            data.setdefault(
                'subOrderAmount', str(sub_order_money.amount)
            )
        if ci := kwargs.get('certId'):
            data.setdefault('certId', self.encrypt_sensitive_information(ci))
            data.setdefault(
                'name',
                self.encrypt_sensitive_information(kwargs.get('name'))
            )

        ts, sign = self._sign(data)
        headers = self._build_request_headers(
            ts,
            sign
        )

        response = self._request(
            url,
            data,
            headers
        )

        r = json.loads(response.content)

        if r.get('code') != 1000:
            raise FacadeException(
                message=r.get('msg')
            )

        return r

    def query_alipay_declaration(self, **kwargs):

        """ 支付宝报关查询 """

        logger.info(f'TEPay.TEPay.query_alipay_declaration.**kwargs: {kwargs}')

        url = f'{self._gateway}/V1/customs/declareQuery'

        data = {}

        if son := kwargs.get('subOrderNo'):
            data.setdefault('subOrderNo', son)

        if otn := kwargs.get('outTradeNo'):
            data.setdefault('outTradeNo', otn)

        ts, sign = self._sign(data)
        headers = self._build_request_headers(
            ts,
            sign
        )

        response = self._request(
            url,
            data,
            headers
        )

        r = json.loads(response.content)

        if r.get('code') != 1000:
            raise FacadeException(
                message=r.get('msg')
            )

        return r

    def encrypt_sensitive_information(self, message=''):

        """ 敏感数据加密 """

        with open(self._publickey_path, 'r') as f:

            pk = f.read()

            pk = rsa.PublicKey.load_pkcs1_openssl_pem(pk.encode('utf8'))

            return b64encode(
                rsa.encrypt(message.encode('utf8'), pk)
            ).decode('utf8')
