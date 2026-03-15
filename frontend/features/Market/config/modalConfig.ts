import type { MarketContextType } from '@/lib/contexts/MarketContext';
import type { DriverWithOwnership } from '@/features/Market/types/marketTypes';

export type ModalMode = 'quickSell' | 'listForSale' | 'buyDriver';

interface ModalModeConfig {
  getDriver: (ctx: MarketContextType) => DriverWithOwnership | null;
  setDriver: (ctx: MarketContextType) => (driver: DriverWithOwnership | null) => void;
  getLoading: (ctx: MarketContextType) => boolean;
}

export const MODAL_MODE_CONFIG: Record<ModalMode, ModalModeConfig> = {
  buyDriver: {
    getDriver: (ctx) => ctx.state.buyModalDriver,
    setDriver: (ctx) => ctx.state.setBuyModalDriver,
    getLoading: (ctx) => ctx.isBuyingFromMarket,
  },
  
  quickSell: {
    getDriver: (ctx) => ctx.state.sellModalDriver,
    setDriver: (ctx) => ctx.state.setSellModalDriver,
    getLoading: (ctx) => ctx.isSellingToMarket,
  },
  
  listForSale: {
    getDriver: (ctx) => ctx.state.listModalDriver,
    setDriver: (ctx) => ctx.state.setListModalDriver,
    getLoading: (ctx) => ctx.isListing,
  },
} as const;
