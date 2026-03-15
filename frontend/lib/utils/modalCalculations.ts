import type { DriverWithOwnership } from '@/lib/types/marketTypes';

interface ModalCalculations {
  acquisitionPrice: number;
  refundAmount: number;
  loss: number;
  price: number;
  budgetAfter: number;
  suggestedPrice: number;
}

interface CalculateModalValuesParams {
  driver: DriverWithOwnership;
  userBudget?: number;
}

export const calculateModalValues = ({
  driver,
  userBudget = 0
}: CalculateModalValuesParams): ModalCalculations => {
  const acquisitionPrice = driver.ownership?.acquisition_price || driver.fantasy_stats?.price || 0;
  
  const refundAmount = Math.floor(acquisitionPrice * 0.8);
  const loss = acquisitionPrice - refundAmount;
  
  const price = driver.fantasy_stats?.price || 0;
  const budgetAfter = userBudget - price;
  
  const suggestedPrice = Math.round(acquisitionPrice * 1.1);

  return {
    acquisitionPrice,
    refundAmount,
    loss,
    price,
    budgetAfter,
    suggestedPrice
  };
};

interface ProfitCalculation {
  profit: number;
  profitPercentage: string;
}

export const calculateProfit = (
  customPrice: number,
  acquisitionPrice: number
): ProfitCalculation => {
  const profit = customPrice - acquisitionPrice;
  const profitPercentage = acquisitionPrice > 0 
    ? ((profit / acquisitionPrice) * 100).toLocaleString(undefined, { 
        maximumFractionDigits: 6, 
        useGrouping: false 
      }) 
    : '0.0';

  return {
    profit,
    profitPercentage
  };
};
