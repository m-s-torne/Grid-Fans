import { motion } from 'framer-motion';
import { useDriverSaleModal } from '@/features/Market/hooks';
import { DriverSaleModalHeader } from './DriverSaleModalHeader';
import { DriverSaleModalInfo } from './DriverSaleModalInfo';
import { CantProceedBadge } from './CantProceedBadge';
import { DriverSaleModalActions } from './DriverSaleModalActions';
import { useMarketContext } from '@/core/contexts/MarketContext';
import { TransactionDetails } from './TransactionDetails';
import { MODAL_MODE_CONFIG, type ModalMode } from '@/features/Market/config/modalConfig';

interface DriverSaleModalProps {
  mode: ModalMode;
}

export const DriverSaleModal = ({
  mode,
}: DriverSaleModalProps) => {
  const marketContext = useMarketContext();
  // Para añadir un nuevo modo, solo editas modalConfig.ts
  const config = MODAL_MODE_CONFIG[mode];
  const driver = config.getDriver(marketContext);
  const onCancel = config.setDriver(marketContext);
  const loading = config.getLoading(marketContext);

  // Early return si no hay driver
  if (!driver) return null;

  const {
    customPrice,
    error,
    canProceed,
    config: modalConfig,
    handleConfirm,
    acquisitionPrice,
    inputValue,
    profit,
    profitPercentage,
    handlePriceChange,
    handlePresetClick,
    price,
    budgetAfter,
    refundAmount,
    loss,
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
            <DriverSaleModalHeader
                driver={driver}
                mode={mode}
                icon={modalConfig.icon}
                iconBorderColor={modalConfig.iconBorderColor}
                iconBgColor={modalConfig.iconBgColor}
                title={modalConfig.title}
                subtitle={modalConfig.subtitle}
                onCancel={() => onCancel(null)}
            />

          {/* Content */}
          <div className="px-5 py-3 space-y-2.5">
            {/* Driver Info */}
            <DriverSaleModalInfo driver={driver} />

            {/* Transaction Details */}
            <TransactionDetails 
                mode={mode}
                driver={driver}
                acquisitionPrice={acquisitionPrice}
                inputValue={inputValue}
                error={error}
                profit={profit}
                profitPercentage={profitPercentage}
                handlePriceChange={handlePriceChange}
                handlePresetClick={handlePresetClick}
                isListing={marketContext.isListing}
                userBudget={marketContext.userState.userBudget}
                price={price}
                budgetAfter={budgetAfter}
                refundAmount={refundAmount}
                loss={loss}
            />

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
                  {modalConfig.infoText}
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
            buttonColor={modalConfig.buttonColor}
            buttonText={modalConfig.buttonText}
            onCancel={() => onCancel(null)}
            onConfirm={handleConfirm}
          />
        </div>
      </motion.div>
    </>
  );
};
