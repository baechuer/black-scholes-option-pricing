<template>
  <div class="flex h-screen">
    <!-- Form Container (30% width) -->
    <div class="w-[30%] p-6 bg-my-blue-1 border-r border-gray-200 overflow-y-auto">
      <h2 class="text-2xl font-bold text-gray-800 mb-6">Options Pricing Calculator</h2>
      
      <form @submit.prevent="calculatePrice" class="space-y-4">
        <!-- Spot Price -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Spot Price ($)</label>
          <input 
            v-model.number="form.spot_price" 
            type="number" 
            step="0.01" 
            min="0.01" 
            required
            class="w-full px-3 py-2  border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
        </div>

        <!-- Strike Price -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Strike Price ($)</label>
          <input 
            v-model.number="form.strike" 
            type="number" 
            step="0.01" 
            min="0.01" 
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
        </div>

        <!-- Time to Expiry -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Time to Expiry (years)</label>
          <input 
            v-model.number="form.time_to_expiry" 
            type="number" 
            step="0.01" 
            min="0.01" 
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
        </div>

        <!-- Risk-Free Rate -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Risk-Free Rate (%)</label>
          <input 
            v-model.number="form.risk_free_rate" 
            type="number" 
            step="0.01" 
            min="0" 
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
        </div>

        <!-- Volatility -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Volatility (%)</label>
          <input 
            v-model.number="form.volatility" 
            type="number" 
            step="0.01" 
            min="0.01" 
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
        </div>

        <!-- Option Type -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Option Type</label>
          <select 
            v-model="form.option_type"
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="call">Call</option>
            <option value="put">Put</option>
          </select>
        </div>

        <!-- Submit Button -->
        <button 
          type="submit" 
          :disabled="isLoading"
          class="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ isLoading ? 'Calculating...' : 'Calculate Price' }}
        </button>
      </form>

      <!-- Results -->
      <div v-if="result" class="mt-6 p-4 bg-green-50 rounded-md border border-green-200">
        <h3 class="text-lg font-medium text-green-800">Option Price:</h3>
        <p class="text-2xl font-bold text-green-600 mt-1">${{ result.price.toFixed(2) }}</p>
        <div class="mt-2 text-sm text-green-700">
          <p>Type: {{ form.option_type === 'call' ? 'Call' : 'Put' }}</p>
          <p>Calculation Time: {{ new Date().toLocaleTimeString() }}</p>
        </div>
      </div>

      <!-- Error Message -->
      <div v-if="error" class="mt-6 p-4 bg-red-50 rounded-md border border-red-200">
        <p class="text-sm font-medium text-red-800">{{ error }}</p>
      </div>
    </div>

    <!-- Right Side Content (70% width) -->
    <div class="w-[70%] p-6 bg-my-blue-3 overflow-y-auto">
      <h2 class="text-2xl font-bold text-gray-800 mb-6">Analysis Results</h2>
      <div class="rounded-lg p-4 h-full">
        <p class="text-gray-600">Visualizations and detailed analysis will appear here.</p>
        <!-- You can add charts, tables, or other visualizations here -->
      </div>
    </div>
  </div>
</template>

<script>
import { calculateOptionPrice } from '@/services/optionPricingService.js';

export default {
  data() {
    return {
      form: {
        spot_price: 100,
        strike: 100,
        time_to_expiry: 1,
        risk_free_rate: 5,  // Represented as percentage (5 for 5%)
        volatility: 20,     // Represented as percentage (20 for 20%)
        option_type: 'call'
      },
      result: null,
      error: null,
      isLoading: false
    };
  },
  methods: {
    async calculatePrice() {
      this.isLoading = true;
      this.error = null;
      this.result = null;
      
      try {
        // Convert percentages to decimals for calculation
        const payload = {
          ...this.form,
          risk_free_rate: this.form.risk_free_rate / 100,
          volatility: this.form.volatility / 100
        };

        // Here you would call your API
        // const response = await optionPricingService.calculateOptionPrice(payload);
        
        // Mock response for demonstration
        const response = await calculateOptionPrice(payload);
        this.result = response.data;
      } catch (error) {
        this.error = error.response?.data?.error || error.message || 'Calculation failed';
      } finally {
        this.isLoading = false;
      }
    },
    calculateMockPrice() {
      // Simple mock calculation for demonstration
      const { spot_price, strike, time_to_expiry, volatility, option_type } = this.form;
      const intrinsic = option_type === 'call' 
        ? Math.max(0, spot_price - strike) 
        : Math.max(0, strike - spot_price);
      
      const timeValue = volatility * Math.sqrt(time_to_expiry);
      return intrinsic + timeValue;
    }
  }
};
</script>

<style scoped>
/* You can add custom styles here if needed */
</style>