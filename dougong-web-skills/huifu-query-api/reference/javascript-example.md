# 交易查询接口 - JavaScript 示例

## 基础调用示例

```javascript
const handleQuery = async (huifuId, orgReqDate, orgReqSeqId) => {
  try {
    const response = await fetch('/hfpay/queryorderinfo', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        huifuId,
        org_req_date: orgReqDate,
        org_req_seq_id: orgReqSeqId
      })
    })

    const result = await response.json()

    if (result.respCode === '00000000') {
      return result.data
    } else {
      throw new Error(result.respDesc || '查询失败')
    }
  } catch (error) {
    console.error('查询错误:', error)
    throw error
  }
}
```

## 使用示例

```javascript
const queryTransaction = async () => {
  try {
    const transaction = await handleQuery(
      '6666000109133323', // 请替换为您自己的汇付商户号
      '20260310',
      '20260310213157551a24fbwn704exdo'
    )
    console.log('交易详情:', transaction)
  } catch (error) {
    console.error('查询失败:', error.message)
  }
}
```
