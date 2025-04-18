<template>
  <div class="flex h-screen">
    <!-- Form Container (30% width) -->
    <div class="w-[22%] p-6 bg-my-blue-3 border-r border-gray-200 overflow-y-auto">
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
          class="w-full py-2 px-4 bg-red-600 hover:bg-red-700 text-white font-medium rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ isLoading ? 'Calculating...' : 'Calculate Price' }}
        </button>
      </form>


    </div>

    <!-- Right Side Content (70% width) -->
    <div class="w-[78%] p-6 bg-my-blue-1 overflow-y-auto">
      <h2 class="text-2xl font-bold text-gray-800 mb-6">Analysis Results</h2>
      <div class="rounded-lg p-4 h-full">
        <p class="text-gray-600">Visualizations and detailed analysis will appear here.</p>
        <!-- You can add charts, tables, or other visualizations here -->
        <!-- Results -->
        <div v-if="result" class="mt-6 p-4 bg-green-50 rounded-md border border-green-200">
          <h3 class="text-lg font-medium text-green-800">Option Price:</h3>
          <div class="flex">
              <p class="text-2xl font-bold text-green-600 mt-1">${{ result.price.toFixed(2) }}</p>
            <div class="mt-2 text-sm text-green-700 flex">
              <p class="ml-2">Type: {{ form.option_type === 'call' ? 'Call' : 'Put' }}</p>
              <p class="ml-2">Calculation Time: {{ new Date().toLocaleTimeString() }}</p>
            </div>
          </div>

        </div>

        <!-- Error Message -->
        <div v-if="error" class="mt-6 p-4 bg-red-50 rounded-md border border-red-200">
          <p class="text-sm font-medium text-red-800">{{ error }}</p>
        </div>

        <div v-if="greek_result" class="mt-6 p-4 bg-green-50 rounded-md border border-green-200">
          <h3 class="text-lg font-medium text-green-800">Greeks:</h3>
          <div class=" flex flex-wrap">
            <div v-for="(value, greek) in greek_result" :key="greek" class="flex items-center mr-2">
              <div class="p-1 bg-green-50 rounded-md border border-green-200 flex hover:bg-green-100 transition ease-in duration 50">
                <p class="text-green-800 font-bold">{{ greek }} ({{ getGreekSymbol(greek) }}):  </p>
                <p class="ml-2 text-green-800">  {{ value.toFixed(4) }}</p>
              </div>

            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { calculateOptionPrice } from '@/services/optionPricingService.js';
import { calculateGreeks } from '@/services/optionPricingService.js';

import debounce from 'lodash.debounce';

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
      isLoading: false,
      greek_result: null
    };
  },
  created() {
    this.debouncedCalculate = debounce(this.calculatePrice, 500);
  },
  watch: {
    form: {
      handler(newValue) {
        if (
          newValue.spot_price > 0 &&
          newValue.strike > 0 &&
          newValue.time_to_expiry > 0
        ) {
          this.debouncedCalculate();
        }
      },
      deep: true,
    },
  },
  methods: {
    async calculateGreek(){
      this.isLoading = true;
      this.error = null;
      this.greek_result = null;

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
        const response = await calculateGreeks(payload);
        this.greek_result = response.data;
      } catch (error) {
        this.error = error.response?.data?.error || error.message || 'Calculation failed';
      } finally {
        this.isLoading = false;
      }
    },
    async calculatePrice() {
      this.isLoading = true;
      this.error = null;
      this.result = null;
      this.calculateGreek()
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
    getGreekSymbol(greek) {
      const symbols = {
        delta: 'Δ',
        gamma: 'Γ',
        vega: 'ν',
        theta: 'Θ',
        rho: 'ρ'
      };
      return symbols[greek] || '';
    },


  }
};
</script>

<style scoped>
/* You can add custom styles here if needed */
</style>