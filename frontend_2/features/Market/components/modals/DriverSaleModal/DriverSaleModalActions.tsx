type ModalMode = 'quickSell' | 'listForSale' | 'buyDriver';

interface DriverSaleModalActionsProps {
  mode: ModalMode;
  loading: boolean;
  canProceed: boolean;
  error: string | null;
  customPrice: number;
  buttonColor: string;
  buttonText: string;
  onCancel: () => void;
  onConfirm: () => void;
}

export const DriverSaleModalActions = ({
  mode,
  loading,
  canProceed,
  error,
  customPrice,
  buttonColor,
  buttonText,
  onCancel,
  onConfirm
}: DriverSaleModalActionsProps) => {
  return (
    <div className="px-5 py-3 flex gap-2.5">
      <button
        onClick={onCancel}
        disabled={loading}
        className="flex-1 px-4 py-2.5 bg-gray-700 hover:bg-gray-600 text-white rounded-lg text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Cancel
      </button>
      <button
        onClick={onConfirm}
        disabled={loading || !canProceed || (mode === 'listForSale' && (!!error || customPrice <= 0))}
        className={`flex-1 px-3 sm:px-4 py-2.5 ${buttonColor} text-white rounded-lg text-[10px] sm:text-sm font-medium transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-1.5 sm:gap-2 min-w-0`}
      >
        {loading ? (
          <>
            <div className="w-3.5 h-3.5 sm:w-4 sm:h-4 border-2 border-white/30 border-t-white rounded-full animate-spin flex-shrink-0" />
            <span>
              {mode === 'quickSell' ? 'Selling...' : mode === 'buyDriver' ? 'Processing...' : 'Listing...'}
            </span>
          </>
        ) : (
          <>
            {mode === 'quickSell' ? (
              <svg className="w-3.5 h-3.5 sm:w-4 sm:h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            ) : mode === 'buyDriver' ? (
              <svg className="w-3.5 h-3.5 sm:w-4 sm:h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            ) : null}
            <span>{buttonText}</span>
          </>
        )}
      </button>
    </div>
  );
};
