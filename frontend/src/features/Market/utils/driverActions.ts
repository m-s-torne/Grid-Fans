/**
 * Pure utility functions for determining driver card actions
 * No React dependencies - pure business logic
 */
import type { DriverWithOwnership } from '../types/marketTypes';
import type { DriverPricing } from './driverPricing';

export type ActionButtonType = 
  | 'buy-free-agent'
  | 'unlist'
  | 'sell-options'
  | 'buy-listed'
  | 'buyout'
  | 'locked-by-me'
  | 'locked-by-other';

export interface DriverCardActions {
  actionType: ActionButtonType;
  canAfford: boolean;
  canAffordBuyout: boolean;
  hasSpace: boolean;
  canExecuteAction: boolean;
  priceToCheck: number;
}

/**
 * Determine what action button should be shown and if it can be executed
 * Pure function - business logic only
 */
export function determineDriverAction(
  pricing: DriverPricing,
  userBudget: number,
  userDriverCount: number
): DriverCardActions {
  const {
    isFreeAgent,
    isOwnedByMe,
    isOwnedByOther,
    isLocked,
    isForSale,
    basePrice,
    displayPrice,
    buyoutPrice,
  } = pricing;

  // Calculate affordability
  const priceToCheck = isFreeAgent ? basePrice : displayPrice;
  const canAfford = userBudget >= priceToCheck;
  const canAffordBuyout = userBudget >= buyoutPrice;
  const hasSpace = userDriverCount < 4;

  // Determine action type and executability
  let actionType: ActionButtonType;
  let canExecuteAction = false;

  if (isFreeAgent) {
    actionType = 'buy-free-agent';
    canExecuteAction = canAfford && hasSpace;
  } else if (isOwnedByMe) {
    if (isLocked) {
      actionType = 'locked-by-me';
      canExecuteAction = false;
    } else if (isForSale) {
      actionType = 'unlist';
      canExecuteAction = true;
    } else {
      actionType = 'sell-options';
      canExecuteAction = true;
    }
  } else if (isOwnedByOther) {
    if (isForSale) {
      actionType = 'buy-listed';
      canExecuteAction = canAfford && hasSpace;
    } else if (!isLocked) {
      actionType = 'buyout';
      canExecuteAction = canAffordBuyout && hasSpace;
    } else {
      actionType = 'locked-by-other';
      canExecuteAction = false;
    }
  } else {
    actionType = 'locked-by-other';
    canExecuteAction = false;
  }

  return {
    actionType,
    canAfford,
    canAffordBuyout,
    hasSpace,
    canExecuteAction,
    priceToCheck,
  };
}

export const getDriverValues = (driver: DriverWithOwnership, pricing: DriverPricing, reserveDriverId: number | null) => {
  const { isOwnedByMe, isLocked } = pricing;
  const ownership = driver.ownership;
  const isReserve = isOwnedByMe && reserveDriverId === driver.id;

  return {
    ownership,
    isReserve,
    isLocked
  }
}
