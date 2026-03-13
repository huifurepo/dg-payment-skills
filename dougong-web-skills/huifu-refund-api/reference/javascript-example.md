# 退款接口 - JavaScript 示例

## 基础调用示例

```javascript
const handleRefund = async (huifuId, ordAmt, orgReqDate, orgReqSeqId) => {
  try {
    const response = await fetch('/hfpay/htRefund', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        huifuId,
        ord_amt: ordAmt,
        org_req_date: orgReqDate,
        org_req_seq_id: orgReqSeqId
      })
    })

    const result = await response.json()

    if (result.respCode === '00000000') {
      return { success: true, message: '退款申请成功' }
    } else {
      return { success: false, message: result.respDesc || '退款申请失败' }
    }
  } catch (error) {
    console.error('退款错误:', error)
    return { success: false, message: '网络请求失败，请检查网络连接' }
  }
}
```

## 使用示例

```javascript
const processRefund = async () => {
  const result = await handleRefund(
    '6666000109133323', // 请替换为您自己的汇付商户号
    '0.10',
    '20260310',
    '20260310213157551a24fbwn704exdo'
  )
  
  if (result.success) {
    console.log('退款成功:', result.message)
  } else {
    console.error('退款失败:', result.message)
  }
}
```
