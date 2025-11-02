import { useMarketContext } from '@/core/contexts/MarketContext';
import { useDriverSaleModal } from '@/features/Market/hooks';
import type { ModalMode } from './modalConfig';

interface DriverSaleModalHeaderProps {
  mode: ModalMode;
}

export const DriverSaleModalHeader = ({
  mode
}: DriverSaleModalHeaderProps) => {
  const {
    buyModalDriver,
    sellModalDriver,
    listModalDriver,
    setBuyModalDriver,
    setSellModalDriver,
    setListModalDriver
  } = useMarketContext()

  const onCancel = mode === 'buyDriver' ? () => setBuyModalDriver(null)
    : mode === 'quickSell' ? () => setSellModalDriver(null)
    : () => setListModalDriver(null)

  const driver = mode === 'buyDriver' 
    ? buyModalDriver
    : mode === 'quickSell'
    ? sellModalDriver
    : mode === 'listForSale'
    ? listModalDriver : null

  const {
    config
  } = useDriverSaleModal({ driver, mode })

  return (
    <div className="px-5 py-4 border-b border-gray-700">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          {mode === 'quickSell' || mode === 'buyDriver' ? (
            <div className={`w-10 h-10 rounded-full ${config.iconBgColor} border ${config.iconBorderColor} flex items-center justify-center`}>
              {typeof config.icon === 'string' ? (
                <span className="text-xl">{config.icon}</span>
              ) : (
                config.icon
              )}
            </div>
          ) : (
            <div className="text-2xl">{config.icon}</div>
          )}
          <div>
            <h2 className="text-xl font-bold text-white">{config.title}</h2>
            <p className="text-gray-400 text-xs">{config.subtitle}</p>
          </div>
        </div>
        <button
          onClick={onCancel}
          className="text-gray-400 hover:text-white transition-colors"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>
  );
};
