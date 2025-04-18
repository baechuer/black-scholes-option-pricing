import axios from 'axios';

export function calculateOptionPrice(data) {
  return axios.post('http://localhost:5000/api/pricing/option_price', data);
}

export function calculateGreeks(data) {
  return axios.post('http://localhost:5000/api/pricing/calc_greeks', data);

}