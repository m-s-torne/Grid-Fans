import type { MarketContext } from '@/core/contexts/MarketContext';
import type { DriverWithOwnership } from '@/features/Market/types/marketTypes';

export type ModalMode = 'quickSell' | 'listForSale' | 'buyDriver';

/**
 * Configuración para cada modo del modal
 * Centraliza la lógica de acceso a datos según el modo
 */
interface ModalModeConfig {
  /** Obtiene el driver del contexto según el modo */
  getDriver: (ctx: MarketContext) => DriverWithOwnership | null;
  
  /** Obtiene la función para setear/cancelar el driver */
  setDriver: (ctx: MarketContext) => (driver: DriverWithOwnership | null) => void;
  
  /** Obtiene el estado de loading según el modo */
  getLoading: (ctx: MarketContext) => boolean;
}

/**
 * ✅ SINGLE SOURCE OF TRUTH para la configuración de cada modo
 * 
 * Para añadir un nuevo modo (ej: 'trade'):
 * 1. Añade el tipo a ModalMode: 'quickSell' | 'listForSale' | 'buyDriver' | 'trade'
 * 2. Añade su configuración aquí
 * 3. ¡Listo! No necesitas modificar DriverSaleModal.tsx
 */
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