# -*- coding: utf-8 -*-
# @Time : 2022/5/20下午13:14
# @Author : anwen
# @Email : anwen@transfereasy.com
# @FileName : api_test.py
# @Software: PyCharm
from tepay.tepay import TEPay
from config.__dev import DEBUG


tepay = TEPay(
    product_code='CP0001',      # 产品编号
    hp_mchid='80000138',        # 商户号
    channel_mchid='80000001',   # 子商户号
    pub_path='/Users/aw/te_admin_python_sdk/config/CERTID_PUBLIC_KEY.pem',     # 共钥
    pri_path='/Users/aw/te_admin_python_sdk/config/80000138_PRIVATE_KEY.pem',    # 私钥
    facade_config='your_notify_url',    # 异步通知地址  N
    debug=DEBUG     # 是否测试
)


def V1_transaction_payment():
    params = {
        'outTradeNo': 'AW202208171552301',        # 商户交易流水号  Y
        'amount': 100,                           # 支付单金额，单位为元，精度最多小数点后两位(如果是JPY和KRW，单位为分) Y
        'currency': 'HKD',                       # 结算币种 Y
        'tradeType': 'WEB',                      # 支付方式
        'productInfo': [
            {
                "amount": 20,
                "description": "测试商品 1 个",
                "name": "测试商品",
                "quantity": 1
            },
            {
                "amount": 20,
                "description": "测试商品 1 个",
                "name": "测试商品 2",
                "quantity": 1
            }
        ],                    # 商品信息 Y
        'clientIp': '0.0.0.0',                   # 客户端设备IP地址 Y
        'settleCurrency': 'USD',                 # 结算币种
    }
    tepay.payment(**params)


def V1_transaction_searchPayment():
    params = {
        'payment_no': 'AW202208171552301',        # 商户交易流水号  Y
    }
    tepay.query_payment(**params)


def V1_transaction_closePayment():
    params = {
        'payment_no': 'AW202208171552301',        # 商户交易流水号  Y
    }
    tepay.close_payment(**params)


def V1_transaction_consultPayment():
    params = {
        'amount': 100,                           # 支付单金额，单位为元，精度最多小数点后两位(如果是JPY和KRW，单位为分) Y
        'currency': 'USD',                       # 结算币种 Y
        "presentmentMode": 'TILE',
        'tradeType': 'WEB',                      # 支付方式
        'settleCurrency': 'USD',                 # 结算币种

    }
    tepay.consult_payment(**params)


def V1_transaction_searchRate():
    params = {
        'feeType': 'USD',                      # 币种
        'date': '20220818',                    # 日期
    }
    tepay.search_rate(**params)


def V1_transaction_refund():
    params = {
        'outTradeNo': 'DE20220808150004',      # 单号
        'paymentNo': '20220808150014P6731',       # 原支付单号
        'refundAmount': '1000',      # 金额
        'remark': '测试一笔退款',     # 备注
    }
    tepay.refund(**params)


def V1_transaction_searchRefund():
    params = {
        "outTradeNo": "DE20220808150004"
    }
    tepay.refund_query(**params)


def bill_download():
    params = {
        'billDate': '2022-03-23',
        'currency': 'HKD'
    }
    tepay.download_bill(**params)


def V1_customs_declare():
    params = {
        'outTradeNo': 'DE20220808150004',
        'paymentNo': '20220808150014P6731',
        'customs': 'SHENZHEN',
        'merchantCustomsCode': 'XXXX',
        'merchantCustomsName': 'XXXX',
        'isSplit': 'false',
        'certId': '140000000000001832',
        'name': 'aw'
    }
    tepay.alipay_declaration(**params)


def V1_custons_declareQuery():
    """
    以下二个订单号二选一，若拆单则传 subOrderNo，若未拆单则传 outTradeNo
    :return:
    """
    params = {
        'outTradeNo': 'DE20220808150004',
        # 'subOrderNo': '20220808150014P6731',
    }
    tepay.query_alipay_declaration(**params)


if __name__ == '__main__':
    # V1_transaction_consultPayment()   # 2.TransferEasy跨境收单钱包列表查询接口
    # V1_transaction_search_rate()      # 3.TransferEasy 人民币参考汇率查询接口
    # V1_transaction_payment()          # 4.TransferEasy 跨境收单下单提交接口
    # V1_transaction_searchPayment()    # 5.TransferEasy 跨境收单订单查询接口
    # V1_transaction_closePayment()     # 6.TransferEasy 跨境收单订单取消接口
    # V1_transaction_refund()           # 7.TransferEasy 跨境收单退款接口
    # V1_transaction_searchRefund()     # 8.TransferEasy 跨境收单退款查询接口
    # bill_download()                   # 9.TransferEasy 跨境收单导出对账单接口
    V1_customs_declare()              # 10. TransferEasy 跨境收单报关接口     11. TransferEasy 跨境收单报关重推接口
    # V1_custons_declareQuery()           # 12. TransferEasy 跨境收单报关查询接口




