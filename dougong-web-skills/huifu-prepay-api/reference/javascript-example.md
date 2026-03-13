# 预支付接口 - JavaScript 示例

## 基础调用示例

```javascript
const handlePrePay = async (product) => {
  try {
    const response = await fetch('/hfpay/preOrder', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        huifuId: '6666000109133323', // 请替换为您自己的汇付商户号
        transAmt: product.price.toFixed(2),
        goodsDesc: product.name,
      }),
    })

    const result = await response.json()

    if (result.respCode === '00000000' && result.data?.jump_url) {
      window.location.href = result.data.jump_url
    } else {
      console.error(result.respDesc || '支付请求失败')
    }
  } catch (error) {
    console.error('支付请求错误:', error)
  }
}
```

## 响应数据结构

```javascript
{
  "respCode": "00000000",
  "respDesc": "操作成功",
  "uniqueId": "d4b7ee5942904bfdab0f8c53340aa578",
  "data": {
    "time_expire": "20260310214157",
    "hosting_data": "{\"project_id\":\"PROJECTID2023101225142567\",\"project_title\":\"收银台标题\",\"request_type\":\"P\",\"callback_url\":\"https://paas.huifu.com\",\"private_info\":\"商户私有信息test\"}",
    "resp_desc": "操作成功",
    "pre_order_id": "H202603102131570034276413",
    "trans_amt": "0.10",
    "goods_desc": "dawanji",
    "pre_order_type": "1",
    "jump_url": "https://api.huifu.com/hostingh5/?jump_id=H202603102131570034276413&huifu_id=6666000109133323&bank_switch=Y",
    "usage_type": "P",
    "req_seq_id": "20260310213157551a24fbwn704exdo",
    "product_id": "YYZY",
    "req_date": "20260310",
    "resp_code": "00000000",
    "huifu_id": "6666000109133323",
    "order_type": "HT",
    "current_time": "20260310213157"
  }
}
```
