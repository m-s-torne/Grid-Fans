import { useState, useMemo } from 'react';
import { calculateDriverPricing, determineDriverAction, getDriverValues, getPriceInfo } from '@/features/Market/utils';
import type { DriverWithOwnership } from '@/features/Market/types/marketTypes';

interface UseDriverCardLogicParams {
  driver: DriverWithOwnership;
  internalUserId: number;
  reserveDriverId: number | null;
  userBudget: number;
  userDriverCount: number;
}

export const useDriverCardLogic = ({
  driver,
  internalUserId,
  reserveDriverId,
  userBudget,
  userDriverCount,
}: UseDriverCardLogicParams) => {
  const [showSellMenu, setShowSellMenu] = useState(false);

  // Memoize expensive calculations
  const pricing = useMemo(
    () => calculateDriverPricing(driver, internalUserId),
    [driver, internalUserId]
  );

  const actions = useMemo(
    () => determineDriverAction(pricing, userBudget, userDriverCount),
    [pricing, userBudget, userDriverCount]
  );

  const driverValues = useMemo(
    () => getDriverValues(driver, pricing, reserveDriverId),
    [driver, pricing, reserveDriverId]
  );

  const priceInfo = useMemo(
    () => getPriceInfo(pricing),
    [pricing]
  );

  return {
    pricing,
    actions,
    ...driverValues,
    ...priceInfo,
    showSellMenu,
    setShowSellMenu,
  };
};