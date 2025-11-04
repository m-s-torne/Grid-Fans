import { SearchInput } from '@/core/components';
import type { SetStateFunction } from '@/core/contexts/MarketContext';
import type { ActiveTab } from '@/features/Market/hooks/useMarketState';
import type { DriverWithOwnership } from '@/features/Market/types/marketTypes';

interface MarketTabsProp {
    activeTab: ActiveTab | null;
    setActiveTab: SetStateFunction<ActiveTab>;
    searchQuery: string;
    setSearchQuery: SetStateFunction<string>;
    freeDrivers: DriverWithOwnership[] | undefined;
    forSaleDrivers: DriverWithOwnership[] | undefined;
    myDrivers: DriverWithOwnership[] | undefined;
}

export const MarketTabs = ({
    activeTab,
    setActiveTab,
    searchQuery,
    setSearchQuery,
    freeDrivers,
    forSaleDrivers,
    myDrivers
}: MarketTabsProp) => {

    return (
        <div className="bg-gradient-to-br from-gray-800/40 to-gray-900/40 border border-gray-700/50 backdrop-blur-sm rounded-xl sm:rounded-2xl p-4 sm:p-6 mb-6 sm:mb-8">
            {/* Tabs */}
            <div className="flex gap-1 mb-4 sm:mb-6 border-b border-gray-700/50 overflow-hidden">
                <button
                    onClick={() => setActiveTab('free')}
                    className={`flex-1 sm:flex-none sm:px-6 py-2 sm:py-3 text-[11px] sm:text-base font-medium transition-all cursor-pointer whitespace-nowrap ${
                        activeTab === 'free'
                            ? 'text-blue-400 border-b-2 border-blue-400'
                            : 'text-gray-400 hover:text-gray-300'
                    }`}
                >
                    <div className="flex items-center justify-center sm:justify-start gap-1 sm:gap-2">
                        <svg className="w-4 h-4 sm:w-5 sm:h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                        </svg>
                        <span className="hidden sm:inline">Free Agents ({freeDrivers!.length})</span>
                        <span className="sm:hidden">Free ({freeDrivers!.length})</span>
                    </div>
                </button>
                <button
                    onClick={() => setActiveTab('for-sale')}
                    className={`flex-1 sm:flex-none sm:px-6 py-2 sm:py-3 text-[11px] sm:text-base font-medium transition-all cursor-pointer whitespace-nowrap ${
                        activeTab === 'for-sale'
                            ? 'text-yellow-400 border-b-2 border-yellow-400'
                            : 'text-gray-400 hover:text-gray-300'
                    }`}
                >
                    <div className="flex items-center justify-center sm:justify-start gap-1 sm:gap-2">
                        <svg className="w-4 h-4 sm:w-5 sm:h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                        </svg>
                        <span className="hidden sm:inline">For Sale ({forSaleDrivers!.length})</span>
                        <span className="sm:hidden">Sale ({forSaleDrivers!.length})</span>
                    </div>
                </button>
                <button
                    onClick={() => setActiveTab('my-drivers')}
                    className={`flex-1 sm:flex-none sm:px-6 py-2 sm:py-3 text-[11px] sm:text-base font-medium transition-all cursor-pointer whitespace-nowrap ${
                        activeTab === 'my-drivers'
                            ? 'text-green-400 border-b-2 border-green-400'
                            : 'text-gray-400 hover:text-gray-300'
                    }`}
                >
                    <div className="flex items-center justify-center sm:justify-start gap-1 sm:gap-2">
                        <svg className="w-4 h-4 sm:w-5 sm:h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                        </svg>
                        <span className="hidden sm:inline">My Drivers ({myDrivers!.length})</span>
                        <span className="sm:hidden">Mine ({myDrivers!.length})</span>
                    </div>
                </button>
            </div>
            
            <SearchInput
                value={searchQuery}
                onChange={setSearchQuery}
                placeholder="Search by driver name, team, or acronym..."
                label="Search Drivers"
                showResultsText={true}
            />
        </div>
    );
};
