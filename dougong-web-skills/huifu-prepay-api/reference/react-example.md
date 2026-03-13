# 预支付接口 - React 示例

## 基础 Hook 示例

```tsx
import { useState } from 'react'

interface Product {
  id: number
  name: string
  price: number
}

interface PrePayResponse {
  respCode: string
  respDesc: string
  uniqueId: string
  data: {
    jump_url: string
    pre_order_id: string
    req_seq_id: string
    req_date: string
    trans_amt: string
    goods_desc: string
    time_expire: string
  }
}

export const usePrePay = (huifuId: string) => {
  const [loading, setLoading] = useState(false)

  const handlePay = async (product: Product) => {
    setLoading(true)

    try {
      const response = await fetch('/hfpay/preOrder', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          huifuId,
          transAmt: product.price.toFixed(2),
          goodsDesc: product.name,
        }),
      })

      const result: PrePayResponse = await response.json()

      if (result.respCode === '00000000' && result.data?.jump_url) {
        window.location.href = result.data.jump_url
        return { success: true, data: result.data }
      } else {
        return { success: false, message: result.respDesc || '支付请求失败' }
      }
    } catch (error) {
      console.error('支付请求错误:', error)
      return { success: false, message: '网络请求失败，请检查网络连接' }
    } finally {
      setLoading(false)
    }
  }

  return { loading, handlePay }
}
```

## 完整组件示例

```tsx
import React, { useState } from 'react'

interface Product {
  id: number
  name: string
  price: number
  image: string
}

const products: Product[] = [
  { id: 1, name: 'iPhone 15 Pro', price: 0.10, image: 'https://example.com/iphone.jpg' },
  { id: 2, name: 'MacBook Air', price: 0.10, image: 'https://example.com/macbook.jpg' },
]

const PrePayComponent: React.FC = () => {
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null)
  const [loading, setLoading] = useState(false)

  const handlePay = async () => {
    if (!selectedProduct) {
      alert('请先选择商品')
      return
    }

    setLoading(true)

    try {
      const response = await fetch('/hfpay/preOrder', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          huifuId: '6666000109133323', // 请替换为您自己的汇付商户号
          transAmt: selectedProduct.price.toFixed(2),
          goodsDesc: selectedProduct.name,
        }),
      })

      const result = await response.json()

      if (result.respCode === '00000000' && result.data?.jump_url) {
        window.location.href = result.data.jump_url
      } else {
        alert(result.respDesc || '支付请求失败，请稍后重试')
      }
    } catch (error) {
      console.error('支付请求错误:', error)
      alert('网络请求失败，请检查网络连接后重试')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="product-list">
      {products.map((product) => (
        <div
          key={product.id}
          className={`product-card ${selectedProduct?.id === product.id ? 'selected' : ''}`}
          onClick={() => setSelectedProduct(product)}
        >
          <img src={product.image} alt={product.name} />
          <div className="product-info">
            <div className="product-name">{product.name}</div>
            <div className="product-price">¥{product.price}</div>
          </div>
        </div>
      ))}

      {selectedProduct && (
        <div className="bottom-bar">
          <div className="selected-info">
            <span className="label">已选商品</span>
            <span className="product-name">{selectedProduct.name}</span>
          </div>
          <div className="right-section">
            <span className="total-price">¥{selectedProduct.price}</span>
            <button
              className="pay-btn"
              onClick={handlePay}
              disabled={loading}
            >
              {loading ? '处理中...' : '立即支付'}
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

export default PrePayComponent
```

## 使用 TypeScript 类型定义

```tsx
interface PrePayRequest {
  huifuId: string
  transAmt: string
  goodsDesc: string
}

interface PrePayData {
  time_expire: string
  hosting_data: string
  resp_desc: string
  pre_order_id: string
  trans_amt: string
  goods_desc: string
  pre_order_type: string
  jump_url: string
  usage_type: string
  req_seq_id: string
  product_id: string
  req_date: string
  resp_code: string
  huifu_id: string
  order_type: string
  current_time: string
}

interface PrePayResponse {
  respCode: string
  respDesc: string
  uniqueId: string
  data: PrePayData
}

const prePay = async (params: PrePayRequest): Promise<PrePayResponse> => {
  const response = await fetch('/hfpay/preOrder', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(params),
  })
  return response.json()
}
```
