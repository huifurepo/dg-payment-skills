# 交易查询接口 - Vue 3 Composition API 示例

## 完整组件示例

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
const errorMessage = ref('')

const handleQuery = async () => {
  if (!form.value.org_req_date || !form.value.org_req_seq_id) {
    errorMessage.value = '请填写完整的查询信息'
    return
  }

  loading.value = true
  errorMessage.value = ''
  transaction.value = null

  try {
    const response = await fetch('/hfpay/queryorderinfo', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        huifuId: form.value.huifuId,
        org_req_date: form.value.org_req_date,
        org_req_seq_id: form.value.org_req_seq_id
      })
    })

    const result = await response.json()

    if (result.respCode === '00000000') {
      transaction.value = result.data
    } else {
      errorMessage.value = result.respDesc || '查询失败'
    }
  } catch (error) {
    console.error('查询错误:', error)
    errorMessage.value = '网络请求失败，请检查网络连接'
  } finally {
    loading.value = false
  }
}

const formatTransStat = (stat) => {
  const statusMap = {
    'S': '成功',
    'F': '失败',
    'P': '处理中',
    'I': '初始化'
  }
  return statusMap[stat] || stat
}

const formatOrderStat = (stat) => {
  const statusMap = {
    '1': '待支付',
    '2': '支付中',
    '3': '支付成功',
    '4': '支付失败',
    '5': '已退款'
  }
  return statusMap[stat] || stat
}
</script>

<template>
  <div class="query-form">
    <div class="form-group">
      <label>汇付ID</label>
      <input type="text" v-model="form.huifuId" placeholder="请输入汇付ID" />
    </div>

    <div class="form-group">
      <label>交易日期</label>
      <input type="text" v-model="form.org_req_date" placeholder="格式：20260310" />
    </div>

    <div class="form-group">
      <label>交易流水号</label>
      <input type="text" v-model="form.org_req_seq_id" placeholder="请输入交易流水号" />
    </div>

    <button class="query-btn" @click="handleQuery" :disabled="loading">
      {{ loading ? '查询中...' : '查询交易' }}
    </button>

    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>
  </div>

  <div v-if="transaction" class="result-section">
    <h2>交易详情</h2>
    <table class="transaction-table">
      <tbody>
        <tr>
          <td class="label">商品描述</td>
          <td class="value">{{ transaction.goods_desc }}</td>
        </tr>
        <tr>
          <td class="label">交易金额</td>
          <td class="value amount">¥{{ transaction.trans_amt }}</td>
        </tr>
        <tr>
          <td class="label">交易状态</td>
          <td class="value">
            <span :class="['status-badge', transaction.trans_stat === 'S' ? 'success' : 'fail']">
              {{ formatTransStat(transaction.trans_stat) }}
            </span>
          </td>
        </tr>
        <tr>
          <td class="label">订单状态</td>
          <td class="value">
            <span :class="['status-badge', transaction.order_stat === '3' ? 'success' : 'fail']">
              {{ formatOrderStat(transaction.order_stat) }}
            </span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
```
