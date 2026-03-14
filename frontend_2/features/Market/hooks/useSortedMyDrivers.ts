import { useMemo } from 'react';
import type { DriverWithOwnership } from '@/features/Market/types/marketTypes';

interface UserTeam {
    driver_1_id?: number | null;
    driver_2_id?: number | null;
    driver_3_id?: number | null;
    reserve_driver_id?: number | null;
}

interface UseSortedMyDriversParams {
    myDrivers?: DriverWithOwnership[];
    userTeam?: UserTeam | null;
}

export const useSortedMyDrivers = ({
    myDrivers,
    userTeam,
}: UseSortedMyDriversParams) => {
    return useMemo(() => {
        if (!myDrivers || !userTeam) return [];
        
        const sorted: DriverWithOwnership[] = [];
        
        const driver1 = myDrivers.find(d => d.id === userTeam.driver_1_id);
        const driver2 = myDrivers.find(d => d.id === userTeam.driver_2_id);
        const driver3 = myDrivers.find(d => d.id === userTeam.driver_3_id);
        const reserve = myDrivers.find(d => d.id === userTeam.reserve_driver_id);
        
        if (driver1) sorted.push(driver1);
        if (driver2) sorted.push(driver2);
        if (driver3) sorted.push(driver3);
        if (reserve) sorted.push(reserve);
        
        return sorted;
    }, [myDrivers, userTeam]);
};
