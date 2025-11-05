/**
 * Pure utility functions for driver pricing calculations
 * No React dependencies - can be used anywhere and easily tested
 */
import type { DriverWithOwnership } from '@/features/Market/types/marketTypes';
import type { PriceType } from '../components/MarketDriverSection/MarketDriverList/PriceDisplay';

export interface DriverPricing {
  basePrice: number;
  acquisitionPrice: number;
  displayPrice: number;
  buyoutPrice: number;
  refundPrice: number;
  isFreeAgent: boolean;
  isOwnedByMe: boolean;
  isOwnedByOther: boolean;
  isLocked: boolean;
  isForSale: boolean;
}

/**
 * Calculate all pricing and ownership information for a driver
 * Pure function - same inputs always produce same outputs
 */
export function calculateDriverPricing(
  driver: DriverWithOwnership,
  currentUserId: number
): DriverPricing {
  const ownership = driver.ownership;
  
  // Ownership status
  const isOwnedByMe = ownership?.owner_id === currentUserId;
  const isOwnedByOther = !!(ownership?.owner_id && ownership.owner_id !== currentUserId);
  const isFreeAgent = !ownership || ownership.owner_id === null;
  const isLocked = !!(ownership?.locked_until && new Date(ownership.locked_until) > new Date());
  const isForSale = !!ownership?.is_listed_for_sale;

  // Calculate prices
  // Use fantasy_stats.price (dynamic market value) as primary source
  // Base market price from fantasy_stats (dynamic price based on performance)
  // Fallback to 0 if not available (should always be calculated by backend)
  const basePrice = driver.fantasy_stats?.price || 0;
  const acquisitionPrice = ownership?.acquisition_price || basePrice;
  
  // For drivers listed for sale, use asking_price; otherwise use acquisition_price
  const displayPrice = isForSale && ownership?.asking_price 
    ? ownership.asking_price 
    : acquisitionPrice;
    
  const buyoutPrice = Math.round(acquisitionPrice * 1.3);
  const refundPrice = Math.round(acquisitionPrice * 0.8);

  return {
    basePrice,
    acquisitionPrice,
    displayPrice,
    buyoutPrice,
    refundPrice,
    isFreeAgent,
    isOwnedByMe,
    isOwnedByOther,
    isLocked,
    isForSale,
  };
}

export const getPriceInfo = (pricing: DriverPricing): { priceType: PriceType, price: number } => {
  const { basePrice, displayPrice, buyoutPrice, isFreeAgent, isOwnedByOther, isLocked, isForSale } = pricing;

  const finalPrice = isFreeAgent 
    ? basePrice 
    : isForSale 
    ? displayPrice 
    : isOwnedByOther && !isLocked 
    ? buyoutPrice 
    : displayPrice;

  const type = isFreeAgent 
    ? 'base' 
    : isForSale 
    ? 'sale' 
    : isOwnedByOther && !isLocked 
    ? 'buyout' 
    : 'base';

  return {
    priceType: type,
    price: finalPrice
  }
}
