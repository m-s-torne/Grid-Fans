import { useMemo } from 'react';
import type { LineupDriver } from '@/features/League/types/leagueTypes';
import type { UserTeam } from '@/lib/services/userTeamService';
import type { DriverWithOwnership } from '@/features/Market/types/marketTypes';
import type { Team } from '@/lib/types';

export const useLeagueTeam = (
    userTeam: UserTeam | undefined,
    myDriversWithOwnership: DriverWithOwnership[] | undefined,
    allTeams: Team[] | undefined
) => {
    const selectedDrivers: LineupDriver[] = useMemo(() => {
        if (!userTeam || !myDriversWithOwnership) return [];
        
        const driverIds = [
            userTeam.driver_1_id,
            userTeam.driver_2_id,
            userTeam.driver_3_id,
            userTeam.reserve_driver_id,
        ];
        
        return driverIds.map(driverId => 
            myDriversWithOwnership.find(d => d.id === driverId)
        ) as LineupDriver[];
    }, [userTeam, myDriversWithOwnership]);
    
    const selectedConstructor = useMemo(() => {
        if (!userTeam || !allTeams) return null;
        return allTeams.find(t => t.id === userTeam.constructor_id) || null;
    }, [userTeam, allTeams]);
    
    const teamValue = useMemo(() => {
        if (!myDriversWithOwnership?.length) return 0;
        return myDriversWithOwnership.reduce((total, driver) => {
            return total + (driver.ownership?.acquisition_price || 0);
        }, 0);
    }, [myDriversWithOwnership]);
    
    return {
        selectedDrivers,
        selectedConstructor,
        teamValue,
    };
};
