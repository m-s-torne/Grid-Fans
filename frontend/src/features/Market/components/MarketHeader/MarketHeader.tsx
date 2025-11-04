import type { NavigateFunction } from 'react-router-dom';
import { DriverSlotsDisplay } from './DriverSlotsDisplay';
import { formatCurrencyPrecise } from '@/features/Market/utils/currencyFormat';
import type { League } from '@/core/services';

interface MarketHeaderProps {
    leagueId: string | undefined;
    league: League;
    userBudget: number;
    userDriverCount: number;
    navigate: NavigateFunction;
}

export const MarketHeader = ({
    leagueId, 
    league,
    userBudget,
    userDriverCount,
    navigate,
}: MarketHeaderProps) => {

    const leagueName = league!.name;

    return (
        <div className="mb-6 sm:mb-8">
            <button
                onClick={() => navigate(`/leagues/${leagueId}`)}
                className="flex items-center text-gray-400 hover:text-white mb-3 sm:mb-4 transition-colors cursor-pointer"
            >
                <svg className="w-4 h-4 sm:w-5 sm:h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
                <span className="text-sm sm:text-base">Back to {leagueName}</span>
            </button>
            
            <div className="flex flex-col gap-4">
                <div>
                    <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-white mb-2">
                        Driver Market
                    </h1>
                    <p className="text-gray-300 text-sm sm:text-base lg:text-lg">
                        Buy, sell, and trade drivers for <span className="text-blue-400 font-medium">{leagueName}</span>
                    </p>
                </div>
                
                {/* Budget & Driver Count */}
                <div className="flex gap-2 sm:gap-4">
                    <div className="
                            w-fit bg-gradient-to-br from-green-600/20 
                            to-green-700/20 border border-green-500/50 
                            rounded-lg sm:rounded-xl px-4 sm:px-6 py-2 sm:py-3
                            flex flex-col items-center 
                    ">
                        <p className="text-green-300 text-xs sm:text-sm font-medium">Budget</p>
                        <p className="text-white text-lg sm:text-2xl font-bold whitespace-nowrap">
                            {formatCurrencyPrecise(userBudget)}
                        </p>
                    </div>
                    <DriverSlotsDisplay driverCount={userDriverCount} />
                </div>
            </div>
        </div>
    );
};
