# 退款接口 - React 示例

## 基础 Hook 示例

```tsx
import { useState } from 'react'

interface RefundParams {
  huifuId: string
  ord_amt: string
  org_req_date: string
  org_req_seq_id: string
}

interface RefundResponse {
  respCode: string
  respDesc: string
}

export const useRefund = () => {
  const [loading, setLoading] = useState(false)

  const refund = async (params: RefundParams): Promise<{ success: boolean; message: string }> => {
    setLoading(true)

    try {
      const response = await fetch('/hfpay/htRefund', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(params),
      })

      const result: RefundResponse = await response.json()

      if (result.respCode === '00000000') {
        return { success: true, message: '退款申请成功' }
      } else {
        return { success: false, message: result.respDesc || '退款申请失败' }
      }
    } catch (error) {
      console.error('退款错误:', error)
      return { success: false, message: '网络请求失败，请检查网络连接' }
    } finally {
      setLoading(false)
    }
  }

  return { loading, refund }
}
```

## 完整组件示例

```tsx
import React, { useState } from 'react'

interface FormData {
  huifuId: string
  org_req_date: string
  org_req_seq_id: string
}

interface Transaction {
  goods_desc: string
  trans_amt: string
  trans_stat: string
  order_stat: string
}

const RefundComponent: React.FC = () => {
  const [form, setForm] = useState<FormData>({
    huifuId: '6666000109133323', // 请替换为您自己的汇付商户号
    org_req_date: '',
    org_req_seq_id: '',
  })

  const [transaction, setTransaction] = useState<Transaction | null>(null)
  const [loading, setLoading] = useState(false)
  const [refundLoading, setRefundLoading] = useState(false)

  const handleQuery = async () => {
    setLoading(true)

    try {
      const response = await fetch('/hfpay/queryorderinfo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      })

      const result = await response.json()

      if (result.respCode === '00000000') {
        setTransaction(result.data)
      }
    } finally {
      setLoading(false)
    }
  }

  const handleRefund = async () => {
    if (!transaction || transaction.order_stat === '5') {
      alert('该订单不可退款')
      return
    }

    if (!window.confirm('确定要申请退款吗？')) return

    setRefundLoading(true)

    try {
      const response = await fetch('/hfpay/htRefund', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          huifuId: form.huifuId,
          ord_amt: transaction.trans_amt,
          org_req_date: form.org_req_date,
          org_req_seq_id: form.org_req_seq_id,
        }),
      })

      const result = await response.json()

      if (result.respCode === '00000000') {
        alert('退款申请成功！')
        setTransaction(null)
      } else {
        alert(result.respDesc || '退款申请失败')
      }
    } catch (error) {
      console.error('退款错误:', error)
      alert('网络请求失败')
    } finally {
      setRefundLoading(false)
    }
  }

  return (
    <div className="refund-container">
      <div className="query-form">
        <div className="form-group">
          <label>汇付ID</label>
          <input
            type="text"
            value={form.huifuId}
            onChange={(e) => setForm({ ...form, huifuId: e.target.value })}
          />
        </div>
        <div className="form-group">
          <label>交易日期</label>
          <input
            type="text"
            value={form.org_req_date}
            onChange={(e) => setForm({ ...form, org_req_date: e.target.value })}
            placeholder="yyyyMMdd"
          />
        </div>
        <div className="form-group">
          <label>交易流水号</label>
          <input
            type="text"
            value={form.org_req_seq_id}
            onChange={(e) => setForm({ ...form, org_req_seq_id: e.target.value })}
          />
        </div>
        <button onClick={handleQuery} disabled={loading}>
          {loading ? '查询中...' : '查询交易'}
        </button>
      </div>

      {transaction && (
        <div className="result-section">
          <h2>交易详情</h2>
          <p>商品: {transaction.goods_desc}</p>
          <p>金额: ¥{transaction.trans_amt}</p>
          <p>订单状态: {transaction.order_stat}</p>

          {transaction.order_stat !== '5' ? (
            <button onClick={handleRefund} disabled={refundLoading}>
              {refundLoading ? '处理中...' : '申请退款'}
            </button>
          ) : (
            <p className="refunded-notice">该订单已退款</p>
          )}
        </div>
      )}
    </div>
  )
}

export default RefundComponent
```

## 结合查询和退款的完整 Hook

```tsx
import { useState, useCallback } from 'react'

interface Transaction {
  goods_desc: string
  trans_amt: string
  trans_stat: string
  order_stat: string
}

interface UseRefundFlowOptions {
  huifuId: string
  onSuccess?: () => void
  onError?: (message: string) => void
}

export const useRefundFlow = (options: UseRefundFlowOptions) => {
  const { huifuId, onSuccess, onError } = options
  const [transaction, setTransaction] = useState<Transaction | null>(null)
  const [queryLoading, setQueryLoading] = useState(false)
  const [refundLoading, setRefundLoading] = useState(false)

  const queryTransaction = useCallback(async (orgReqDate: string, orgReqSeqId: string) => {
    setQueryLoading(true)
    try {
      const response = await fetch('/hfpay/queryorderinfo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          huifuId,
          org_req_date: orgReqDate,
          org_req_seq_id: orgReqSeqId,
        }),
      })

      const result = await response.json()

      if (result.respCode === '00000000') {
        setTransaction(result.data)
        return result.data
      } else {
        onError?.(result.respDesc || '查询失败')
        return null
      }
    } catch (error) {
      onError?.('网络请求失败')
      return null
    } finally {
      setQueryLoading(false)
    }
  }, [huifuId, onError])

  const processRefund = useCallback(async () => {
    if (!transaction) {
      onError?.('请先查询订单')
      return false
    }

    if (transaction.order_stat === '5') {
      onError?.('该订单已退款')
      return false
    }

    if (transaction.order_stat !== '3') {
      onError?.('该订单不可退款')
      return false
    }

    setRefundLoading(true)
    try {
      const response = await fetch('/hfpay/htRefund', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          huifuId,
          ord_amt: transaction.trans_amt,
        }),
      })

      const result = await response.json()

      if (result.respCode === '00000000') {
        setTransaction(null)
        onSuccess?.()
        return true
      } else {
        onError?.(result.respDesc || '退款申请失败')
        return false
      }
    } catch (error) {
      onError?.('网络请求失败')
      return false
    } finally {
      setRefundLoading(false)
    }
  }, [huifuId, transaction, onSuccess, onError])

  const canRefund = transaction && transaction.order_stat === '3'

  return {
    transaction,
    queryLoading,
    refundLoading,
    queryTransaction,
    processRefund,
    canRefund,
    isRefunded: transaction?.order_stat === '5',
  }
}
```
