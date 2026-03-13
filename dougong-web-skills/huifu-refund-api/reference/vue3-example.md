# 退款接口 - Vue 3 Composition API 示例

## 基础组件示例

```vue
<script setup>
import { ref } from 'vue'

const refundLoading = ref(false)

const handleRefund = async (transaction, form) => {
  if (!transaction) return

  if (!confirm('确定要申请退款吗？')) {
    return
  }

  refundLoading.value = true

  try {
    const response = await fetch('/hfpay/htRefund', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        huifuId: form.huifuId,
        ord_amt: transaction.trans_amt,
        org_req_date: form.org_req_date,
        org_req_seq_id: form.org_req_seq_id
      })
    })

    const result = await response.json()

    if (result.respCode === '00000000') {
      alert('退款申请成功！')
      return true
    } else {
      alert(result.respDesc || '退款申请失败')
      return false
    }
  } catch (error) {
    console.error('退款错误:', error)
    alert('网络请求失败，请检查网络连接')
    return false
  } finally {
    refundLoading.value = false
  }
}
</script>

<template>
  <button 
    v-if="transaction.order_stat !== '5'" 
    class="refund-btn" 
    @click="handleRefund(transaction, form)" 
    :disabled="refundLoading"
  >
    {{ refundLoading ? '处理中...' : '申请退款' }}
  </button>
  <div v-else class="refunded-notice">
    该订单已退款
  </div>
</template>
```

## 完整业务流程示例（查询+退款）

```vue
<script setup>
import { ref } from 'vue'

const form = ref({
  huifuId: '6666000109133323', // 请替换为您自己的汇付商户号
  org_req_date: '',
  org_req_seq_id: ''
})

const transaction = ref(null)
const loading = ref(false)
const refundLoading = ref(false)

const handleQuery = async () => {
  loading.value = true
  
  try {
    const response = await fetch('/hfpay/queryorderinfo', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form.value)
    })
    
    const result = await response.json()
    
    if (result.respCode === '00000000') {
      transaction.value = result.data
    }
  } finally {
    loading.value = false
  }
}

const handleRefund = async () => {
  if (!transaction.value || transaction.value.order_stat === '5') {
    alert('该订单不可退款')
    return
  }

  if (!confirm('确定要申请退款吗？')) return

  refundLoading.value = true

  try {
    const response = await fetch('/hfpay/htRefund', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        huifuId: form.value.huifuId,
        ord_amt: transaction.value.trans_amt,
        org_req_date: form.value.org_req_date,
        org_req_seq_id: form.value.org_req_seq_id
      })
    })

    const result = await response.json()

    if (result.respCode === '00000000') {
      alert('退款申请成功！')
      transaction.value = null
    } else {
      alert(result.respDesc || '退款申请失败')
    }
  } catch (error) {
    console.error('退款错误:', error)
    alert('网络请求失败')
  } finally {
    refundLoading.value = false
  }
}
</script>

<template>
  <div class="query-container">
    <div class="query-form">
      <div class="form-group">
        <label>汇付ID</label>
        <input type="text" v-model="form.huifuId" />
      </div>
      <div class="form-group">
        <label>交易日期</label>
        <input type="text" v-model="form.org_req_date" placeholder="yyyyMMdd" />
      </div>
      <div class="form-group">
        <label>交易流水号</label>
        <input type="text" v-model="form.org_req_seq_id" />
      </div>
      <button @click="handleQuery" :disabled="loading">
        {{ loading ? '查询中...' : '查询交易' }}
      </button>
    </div>

    <div v-if="transaction" class="result-section">
      <h2>交易详情</h2>
      <p>商品: {{ transaction.goods_desc }}</p>
      <p>金额: ¥{{ transaction.trans_amt }}</p>
      <p>订单状态: {{ transaction.order_stat }}</p>
      
      <button 
        v-if="transaction.order_stat !== '5'" 
        @click="handleRefund" 
        :disabled="refundLoading"
      >
        {{ refundLoading ? '处理中...' : '申请退款' }}
      </button>
      <p v-else class="refunded-notice">该订单已退款</p>
    </div>
  </div>
</template>
```
