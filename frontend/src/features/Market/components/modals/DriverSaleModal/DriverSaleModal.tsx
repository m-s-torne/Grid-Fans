import { motion } from 'framer-motion';
import { useDriverSaleModal } from '@/features/Market/hooks';
import { DriverSaleModalHeader } from './DriverSaleModalHeader';
import { DriverSaleModalInfo } from './DriverSaleModalInfo';
import { CantProceedBadge } from './CantProceedBadge';
import { DriverSaleModalActions } from './DriverSaleModalActions';
import { useMarketContext } from '@/core/contexts/MarketContext';
import { TransactionDetails } from './TransactionDetails';
import { MODAL_MODE_CONFIG, type ModalMode } from './modalConfig';

interface DriverSaleModalProps {
  mode: ModalMode;
}

export const DriverSaleModal = ({
  mode,
}: DriverSaleModalProps) => {
  const {
    setBuyModalDriver,
    setSellModalDriver,
    setListModalDriver,
    isBuyingFromMarket,
    isSellingToMarket,
    isListing,
    buyModalDriver,
    sellModalDriver,
    listModalDriver
  } = useMarketContext()

  const onCancel = mode === 'buyDriver' ? setBuyModalDriver 
    : mode === 'quickSell' ? setSellModalDriver
    : setListModalDriver

  const loading = mode === 'buyDriver' ? isBuyingFromMarket
    : mode === 'quickSell' ? isSellingToMarket
    : isListing

  const driver = mode === 'buyDriver' 
    ? buyModalDriver
    : mode === 'quickSell'
    ? sellModalDriver
    : mode === 'listForSale'
    ? listModalDriver : null

  if (!driver) return

  const {
    customPrice,
    error,
    canProceed,
    config,
    handleConfirm
  } = useDriverSaleModal({
    driver,
    mode,
  });

  return (
    <>
      {/* Backdrop */}
      <motion.div
        className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50"
        onClick={() => onCancel(null)}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
      />

      {/* Modal */}
      <motion.div
        className="fixed inset-0 flex items-center justify-center z-50 p-4"
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.9 }}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-2xl border border-gray-700 max-w-md w-full shadow-2xl">
          {/* Header */}
          <DriverSaleModalHeader mode={mode}/>

          {/* Content */}
          <div className="px-5 py-3 space-y-2.5">
            {/* Driver Info */}
            <DriverSaleModalInfo mode={mode} />

            {/* Transaction Details */}
            <TransactionDetails mode={mode}/>

            {/* Validation Warning - only for sell/list modes */}
            {!canProceed && mode !== 'buyDriver' && (
              <CantProceedBadge mode={mode} />
            )}

            {/* Info */}
            <div className="bg-blue-900/20 border border-blue-500/30 rounded-lg p-2">
              <div className="flex items-start gap-1.5">
                <svg className="w-4 h-4 text-blue-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p className="text-blue-300 text-[11px]">
                  {config.infoText}
                </p>
              </div>
            </div>
          </div>

          {/* Actions */}
          <DriverSaleModalActions
            mode={mode}
            loading={loading}
            canProceed={canProceed}
            error={error}
            customPrice={customPrice}
            buttonColor={config.buttonColor}
            buttonText={config.buttonText}
            onCancel={() => onCancel(null)}
            onConfirm={handleConfirm}
          />
        </div>
      </motion.div>
    </>
  );
};
