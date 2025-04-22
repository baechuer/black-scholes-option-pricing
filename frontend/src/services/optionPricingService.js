import axios from 'axios';

export function calculateOptionPrice(data) {
  return axios.post('http://localhost:5000/api/pricing/option_price', data);
}

export function calculateGreeks(data) {
  return axios.post('http://localhost:5000/api/pricing/calc_greeks', data);

}
export function getGreekGraph(data) {
  return axios.post('http://localhost:5000/api/pricing/greeks-chart', data);
}
export function getVolatilitySmileByTicket(data) {
  return axios.post('http://localhost:5000/api/market/volatility_smile_by_ticket', data);
}