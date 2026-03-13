# 交易查询接口 - React 示例

## 基础 Hook 示例

```tsx
import { useState } from 'react'

interface QueryParams {
  huifuId: string
  org_req_date: string
  org_req_seq_id: string
}

interface TransactionData {
  mer_name: string
  goods_desc: string
  trans_amt: string
  fee_amt: string
  trans_stat: string
  order_stat: string
  trans_date: string
  pay_type: string
  bank_desc: string
  org_hf_seq_id: string
  req_seq_id: string
}

interface QueryResponse {
  respCode: string
  respDesc: string
  data: TransactionData
}

export const useTransactionQuery = () => {
  const [transaction, setTransaction] = useState<TransactionData | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string>('')

  const query = async (params: QueryParams) => {
    if (!params.org_req_date || !params.org_req_seq_id) {
      setError('请填写完整的查询信息')
      return
    }

    setLoading(true)
    setError('')
    setTransaction(null)

    try {
      const response = await fetch('/hfpay/queryorderinfo', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(params),
      })

      const result: QueryResponse = await response.json()

      if (result.respCode === '00000000') {
        setTransaction(result.data)
        return result.data
      } else {
        setError(result.respDesc || '查询失败')
        return null
      }
    } catch (err) {
      console.error('查询错误:', err)
      setError('网络请求失败，请检查网络连接')
      return null
    } finally {
      setLoading(false)
    }
  }

  return { transaction, loading, error, query }
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
  fee_amt: string
  trans_stat: string
  order_stat: string
  trans_date: string
  pay_type: string
  bank_desc: string
}

const QueryComponent: React.FC = () => {
  const [form, setForm] = useState<FormData>({
    huifuId: '6666000109133323', // 请替换为您自己的汇付商户号
    org_req_date: '',
    org_req_seq_id: '',
  })

  const [transaction, setTransaction] = useState<Transaction | null>(null)
  const [loading, setLoading] = useState(false)
  const [errorMessage, setErrorMessage] = useState('')

  const handleQuery = async () => {
    if (!form.org_req_date || !form.org_req_seq_id) {
      setErrorMessage('请填写完整的查询信息')
      return
    }

    setLoading(true)
    setErrorMessage('')
    setTransaction(null)

    try {
      const response = await fetch('/hfpay/queryorderinfo', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(form),
      })

      const result = await response.json()

      if (result.respCode === '00000000') {
        setTransaction(result.data)
      } else {
        setErrorMessage(result.respDesc || '查询失败')
      }
    } catch (error) {
      console.error('查询错误:', error)
      setErrorMessage('网络请求失败，请检查网络连接')
    } finally {
      setLoading(false)
    }
  }

  const formatTransStat = (stat: string) => {
    const statusMap: Record<string, string> = {
      S: '成功',
      F: '失败',
      P: '处理中',
      I: '初始化',
    }
    return statusMap[stat] || stat
  }

  const formatOrderStat = (stat: string) => {
    const statusMap: Record<string, string> = {
      '1': '待支付',
      '2': '支付中',
      '3': '支付成功',
      '4': '支付失败',
      '5': '已退款',
    }
    return statusMap[stat] || stat
  }

  return (
    <div className="query-container">
      <div className="query-form">
        <div className="form-group">
          <label>汇付ID</label>
          <input
            type="text"
            value={form.huifuId}
            onChange={(e) => setForm({ ...form, huifuId: e.target.value })}
            placeholder="请输入汇付ID"
          />
        </div>

        <div className="form-group">
          <label>交易日期</label>
          <input
            type="text"
            value={form.org_req_date}
            onChange={(e) => setForm({ ...form, org_req_date: e.target.value })}
            placeholder="格式：20260310"
          />
        </div>

        <div className="form-group">
          <label>交易流水号</label>
          <input
            type="text"
            value={form.org_req_seq_id}
            onChange={(e) => setForm({ ...form, org_req_seq_id: e.target.value })}
            placeholder="请输入交易流水号"
          />
        </div>

        <button className="query-btn" onClick={handleQuery} disabled={loading}>
          {loading ? '查询中...' : '查询交易'}
        </button>

        {errorMessage && <div className="error-message">{errorMessage}</div>}
      </div>

      {transaction && (
        <div className="result-section">
          <h2>交易详情</h2>
          <table className="transaction-table">
            <tbody>
              <tr>
                <td className="label">商品描述</td>
                <td className="value">{transaction.goods_desc}</td>
              </tr>
              <tr>
                <td className="label">交易金额</td>
                <td className="value amount">¥{transaction.trans_amt}</td>
              </tr>
              <tr>
                <td className="label">交易状态</td>
                <td className="value">
                  <span className={`status-badge ${transaction.trans_stat === 'S' ? 'success' : 'fail'}`}>
                    {formatTransStat(transaction.trans_stat)}
                  </span>
                </td>
              </tr>
              <tr>
                <td className="label">订单状态</td>
                <td className="value">
                  <span className={`status-badge ${transaction.order_stat === '3' ? 'success' : 'fail'}`}>
                    {formatOrderStat(transaction.order_stat)}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

export default QueryComponent
```
