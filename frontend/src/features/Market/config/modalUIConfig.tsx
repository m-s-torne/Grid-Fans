import type { DriverWithOwnership } from '@/features/Market/types/marketTypes';

export type ModalMode = 'quickSell' | 'listForSale' | 'buyDriver';

export interface ModalUIConfig {
  icon: React.ReactNode | string;
  iconBgColor: string;
  iconBorderColor: string;
  title: string;
  subtitle: string;
  buttonText: string;
  buttonColor: string;
  infoText: string;
}

/**
 * UI Configuration for modal modes
 * Contains icons, colors, texts and styling for each modal type
 */
export const getModalUIConfig = (mode: ModalMode, driver?: DriverWithOwnership | null): ModalUIConfig => {
  switch (mode) {
    case 'quickSell':
      return {
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
      };
      
    case 'listForSale':
      return {
        icon: '💰',
        iconBgColor: 'bg-yellow-600/20',
        iconBorderColor: 'border-yellow-500/50',
        title: 'List for Sale',
        subtitle: `Set your asking price for ${driver?.full_name || 'driver'}`,
        buttonText: 'List for Sale',
        buttonColor: 'bg-yellow-600 hover:bg-yellow-700',
        infoText: 'Listed drivers appear in "For Sale" tab. You can unlist anytime.'
      };
      
    case 'buyDriver':
    default:
      return {
        icon: '💵',
        iconBgColor: 'bg-green-600/20',
        iconBorderColor: 'border-green-500/50',
        title: 'Buy Driver',
        subtitle: 'Confirm purchase',
        buttonText: 'Confirm Purchase',
        buttonColor: 'bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800',
        infoText: 'The driver will be added to your team roster'
      };
  }
};