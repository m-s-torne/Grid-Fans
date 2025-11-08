import { useState } from 'react';
import type { DriverWithOwnership } from '@/features/Market/types/marketTypes';
import { 
  formatCurrencyNumber, 
  parseCurrencyInput, 
  calculateDriverSaleValues, 
  calculateSaleProfit 
} from '@/features/Market/utils';
import { useMarketContext } from '@/core/contexts/MarketContext';
import { getModalUIConfig, type ModalMode } from '@/features/Market/config/modalUIConfig';

interface UseDriverSaleModalProps {
  driver: DriverWithOwnership | null;
  userDriverCount?: number;
  userBudget?: number;
  mode: ModalMode;
}

export const useDriverSaleModal = ({
  driver,
  mode,
}: UseDriverSaleModalProps) => {
  const {
    userState,
    handlers,
  } = useMarketContext()

  // Calculate all financial values
  const {
    acquisitionPrice,
    refundAmount,
    loss,
    price,
    budgetAfter,
    suggestedPrice
  } = calculateDriverSaleValues(driver!, userState.userBudget || 0);
  
  // List for Sale state
  const [inputValue, setInputValue] = useState(formatCurrencyNumber(suggestedPrice));
  const [customPrice, setCustomPrice] = useState(suggestedPrice);
  const [error, setError] = useState<string | null>(null);
  
  // Calculate profit/loss
  const { profit, profitPercentage } = calculateSaleProfit(customPrice, acquisitionPrice);
  
  // Validate minimum drivers (only for sell/list modes)
  const canProceed = mode === 'buyDriver' ? true : (userState.userDriverCount || 0) > 3;
  
  const handlePriceChange = (value: string) => {
    setInputValue(value);
    const numValue = parseCurrencyInput(value);
    if (isNaN(numValue) || numValue <= 0) {
      setError('Please enter a valid price');
      setCustomPrice(0);
      return;
    }
    setCustomPrice(numValue);
    setError(null);
  };
  
  const handlePresetClick = (multiplier: number) => {
    const newPrice = acquisitionPrice * multiplier;
    setInputValue(formatCurrencyNumber(newPrice, 2));
    setCustomPrice(Math.round(newPrice));
    setError(null);
  };
  
  const handleConfirm = () => {
    if (mode === 'listForSale') {
      if (customPrice <= 0) {
        setError('Please enter a valid price');
        return;
      }
      handlers.confirmList(customPrice);
    } else if (mode === 'quickSell') {
      handlers.confirmSell();
    } else {
      handlers.confirmBuyFromMarket();
    }
  };
  
  // Mode-specific config
  const config = getModalUIConfig(mode, driver);

  return {
    // Calculations
    acquisitionPrice,
    refundAmount,
    loss,
    price,
    budgetAfter,
    profit,
    profitPercentage,
    
    // State
    inputValue,
    customPrice,
    error,
    canProceed,
    
    // Config
    config,
    
    // Handlers
    handlePriceChange,
    handlePresetClick,
    handleConfirm
  };
};
