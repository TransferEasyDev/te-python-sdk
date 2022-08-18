

# 全渠道跨境收款

* [商户网站](https://mch.transfereasy.com/)

## 结构

```$xslt
├── config      # 配置文件
├── examples    # DEMO
├── tepay       # API
```

## 示例

```
/**
 * 初始化环境
 */

$ cd te_admin_python_sdk
$ virtualenv ENV
$ source ./ENV/bin/active
$ (ENV) pip install -r requirements.txt
```

```
/**
 * 配置文件
 *
 * └── config
 *     └── __dev.py
 */

# 在 __dev.py 中控制生产和测试的配置文件开关

```

```python
# -*- coding: utf-8 -*-
from tepay.tepay import TEPay
from config.__dev import DEBUG

if __name__ == '__main__':
    tepay = TEPay(
        product_code='产品编号',      # 产品编号
        mchid='you mchid',        # 商户号
        channel_mchid='80000001',   # 子商户号
        pub_path='加密数据使用的公钥路径 CERTID_PUBLIC_KEY.pem',     # 共钥
        pri_path='自己的私钥路径 PRIVATE_KEY.pem',    # 私钥
        facade_config='your notify url',    # 异步通知地址  N
        debug=DEBUG     # 是否测试
    )

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

```

## 依赖

* certifi==2022.6.15
* cffi==1.15.1
* charset-normalizer==2.0.12
* cryptography==3.4.8
* hp-money==1.1.2
* idna==3.3
* pyasn1==0.4.8
* pycparser==2.20
* pycryptodome==3.10.1
* pycryptodomex==3.9.8
* requests==2.26.0
* rsa==4.6
* urllib3==1.26.11
