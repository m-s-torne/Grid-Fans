import type { DriverWithOwnership } from '@/lib/types/marketTypes';

export const calculateDriverSaleValues = (
  driver: DriverWithOwnership,
  userBudget: number = 0
) => {
  const acquisitionPrice = driver.ownership?.acquisition_price || driver.fantasy_stats?.price || 0;
  const price = driver.fantasy_stats?.price || 0;
  
  const refundAmount = Math.floor(acquisitionPrice * 0.8);
  const loss = acquisitionPrice - refundAmount;
  
  const budgetAfter = userBudget - price;
  
  const suggestedPrice = Math.round(acquisitionPrice * 1.1);
  
  return {
    acquisitionPrice,
    price,
    refundAmount,
    loss,
    budgetAfter,
    suggestedPrice
  };
};

export const calculateProfit = (customPrice: number, acquisitionPrice: number) => {
  const profit = customPrice - acquisitionPrice;
  const profitPercentage = acquisitionPrice > 0 
    ? ((profit / acquisitionPrice) * 100).toLocaleString(undefined, { 
        maximumFractionDigits: 6, 
        useGrouping: false 
      }) 
    : '0.0';
  
  return { profit, profitPercentage };
};
