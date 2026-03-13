# 预支付接口 - Vue 3 Composition API 示例

## 完整组件示例

```vue
<script setup>
import { ref } from 'vue'

const loading = ref(false)

const handlePay = async (selectedProduct) => {
  if (!selectedProduct) {
    alert('请先选择商品')
    return
  }

  loading.value = true

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
    loading.value = false
  }
}
</script>
```

## 带商品选择的完整示例

```vue
<script setup>
import { ref } from 'vue'

const products = [
  { id: 1, name: 'iPhone 15 Pro', price: 0.10, image: 'https://example.com/iphone.jpg' },
  { id: 2, name: 'MacBook Air', price: 0.10, image: 'https://example.com/macbook.jpg' },
]

const selectedProduct = ref(null)
const loading = ref(false)

const handleSelect = (product) => {
  selectedProduct.value = product
}

const handlePay = async () => {
  if (!selectedProduct.value) {
    alert('请先选择商品')
    return
  }

  loading.value = true

  try {
    const response = await fetch('/hfpay/preOrder', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        huifuId: 'YOUR_HUIFU_ID',
        transAmt: selectedProduct.value.price.toFixed(2),
        goodsDesc: selectedProduct.value.name,
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
    loading.value = false
  }
}
</script>

<template>
  <div class="product-list">
    <div
      v-for="product in products"
      :key="product.id"
      class="product-card"
      :class="{ selected: selectedProduct?.id === product.id }"
      @click="handleSelect(product)"
    >
      <img :src="product.image" :alt="product.name" />
      <div class="product-info">
        <div class="product-name">{{ product.name }}</div>
        <div class="product-price">¥{{ product.price }}</div>
      </div>
    </div>
  </div>

  <button class="pay-btn" @click="handlePay" :disabled="loading">
    {{ loading ? '处理中...' : '立即支付' }}
  </button>
</template>
```
