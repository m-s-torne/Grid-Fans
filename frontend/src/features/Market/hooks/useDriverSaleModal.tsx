import { useState } from 'react';
import type { DriverWithOwnership } from '@/features/Market/types/marketTypes';
import { 
  formatCurrencyNumber, 
  parseCurrencyInput, 
  calculateDriverSaleValues, 
  calculateSaleProfit 
} from '@/features/Market/utils';
import { useMarketContext } from '@/core/contexts/MarketContext';

type ModalMode = 'quickSell' | 'listForSale' | 'buyDriver';

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
    userDriverCount,
    userBudget,
    confirmBuyFromMarket,
    confirmSell,
    confirmList,
  } = useMarketContext()

  // Calculate all financial values
  const {
    acquisitionPrice,
    refundAmount,
    loss,
    price,
    budgetAfter,
    suggestedPrice
  } = calculateDriverSaleValues(driver!, userBudget || 0);
  
  // List for Sale state
  const [inputValue, setInputValue] = useState(formatCurrencyNumber(suggestedPrice));
  const [customPrice, setCustomPrice] = useState(suggestedPrice);
  const [error, setError] = useState<string | null>(null);
  
  // Calculate profit/loss
  const { profit, profitPercentage } = calculateSaleProfit(customPrice, acquisitionPrice);
  
  // Validate minimum drivers (only for sell/list modes)
  const canProceed = mode === 'buyDriver' ? true : (userDriverCount || 0) > 3;
  
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
      confirmList(customPrice);
    } else if (mode === 'quickSell') {
      confirmSell()
    } else {
      confirmBuyFromMarket();
    }
  };
  
  // Mode-specific config
  const config = mode === 'quickSell' 
    ? {
        icon: (
          <svg className="w-6 h-6 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        ),
        iconBgColor: 'bg-orange-600/20',
        iconBorderColor: 'border-orange-500/50',
        title: 'Quick Sell',
        subtitle: 'Sell driver to market',
        buttonText: 'Confirm Sale',
        buttonColor: 'bg-gradient-to-r from-orange-600 to-red-600 hover:from-orange-500 hover:to-red-500',
        infoText: "The driver will return to the free agent pool and you'll receive 80% of the acquisition price"
      }
    : mode === 'listForSale'
    ? {
        icon: '💰',
        iconBgColor: 'bg-yellow-600/20',
        iconBorderColor: 'border-yellow-500/50',
        title: 'List for Sale',
        subtitle: `Set your asking price for ${driver!.full_name}`,
        buttonText: 'List for Sale',
        buttonColor: 'bg-yellow-600 hover:bg-yellow-700',
        infoText: 'Listed drivers appear in "For Sale" tab. You can unlist anytime.'
      }
    : {
        icon: '💵',
        iconBgColor: 'bg-green-600/20',
        iconBorderColor: 'border-green-500/50',
        title: 'Buy Driver',
        subtitle: 'Confirm purchase',
        buttonText: 'Confirm Purchase',
        buttonColor: 'bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800',
        infoText: 'The driver will be added to your team roster'
      };

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
