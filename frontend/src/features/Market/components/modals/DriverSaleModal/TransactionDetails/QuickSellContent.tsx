import { useDriverSaleModal } from '@/features/Market/hooks';
import { formatCurrencyPrecise } from '@/features/Market/utils';
import type { TransactionDetailsProps } from './TransactionDetails';

export interface QuickSellContentProps {
  acquisitionPrice: number;
  refundAmount: number;
  loss: number;
}

export const QuickSellContent = ({
  acquisitionPrice,
  refundAmount,
  loss,
}: TransactionDetailsProps) => {

  return (
    <div className="bg-gray-700/30 rounded-lg p-3 border border-gray-600/50">
      <div className="flex justify-between items-center mb-1.5">
        <span className="text-gray-400 text-xs">Acquisition Price</span>
        <span className="text-white font-bold text-sm">
          {formatCurrencyPrecise(acquisitionPrice)}
        </span>
      </div>
      <div className="flex justify-between items-center mb-1.5">
        <span className="text-gray-400 text-xs">Refund (80%)</span>
        <span className="text-green-400 font-bold text-sm">
          +{formatCurrencyPrecise(refundAmount)}
        </span>
      </div>
      <div className="border-t border-gray-600/50 pt-1.5 mt-1.5">
        <div className="flex justify-between items-center">
          <span className="text-red-400 text-xs">Loss (20%)</span>
          <span className="text-red-400 font-semibold text-sm">
            -{formatCurrencyPrecise(loss)}
          </span>
        </div>
      </div>
    </div>
  );
};
