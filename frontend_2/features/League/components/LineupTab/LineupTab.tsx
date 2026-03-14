import { LeagueStats } from './LeagueStats';
import { TeamDisplay } from './TeamDisplay';
import type { LineupTabProps } from '@/features/League/types/leagueTypes';

export const LineupTab = ({
    userTeam,
    teamLoading,
    allDriversLoaded,
    allTeamsLoaded,
    selectedDrivers,
    selectedConstructor,
    teamValue,
    onNavigateToMarket
}: LineupTabProps) => {
    if (teamLoading || !allDriversLoaded || !allTeamsLoaded) {
        return (
            <div className="bg-gradient-to-br from-gray-800/40 to-gray-900/40 border border-gray-700/50 backdrop-blur-sm rounded-xl sm:rounded-2xl p-4 sm:p-6 lg:p-8">
                <div className="flex flex-col items-center justify-center py-8 sm:py-12">
                    <div className="animate-spin rounded-full h-10 w-10 sm:h-12 sm:w-12 border-b-2 border-blue-400 mb-4"></div>
                    <p className="text-gray-400 text-sm sm:text-base">Loading your team...</p>
                </div>
            </div>
        );
    }

    if (!userTeam) {
        return (
            <div className="bg-gradient-to-br from-gray-800/40 to-gray-900/40 border border-gray-700/50 backdrop-blur-sm rounded-xl sm:rounded-2xl p-4 sm:p-6 lg:p-8">
                <div className="text-center py-8 sm:py-12">
                    <div className="w-16 h-16 sm:w-20 sm:h-20 mx-auto mb-4 sm:mb-6 bg-gray-700/30 rounded-full flex items-center justify-center">
                        <svg className="w-8 h-8 sm:w-10 sm:h-10 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                        </svg>
                    </div>
                    <h3 className="text-lg sm:text-xl font-semibold text-white mb-2">Build Your Team</h3>
                    <p className="text-gray-400 text-base sm:text-lg mb-2 px-4">Start building your fantasy F1 team!</p>
                    
                    <div className="max-w-md mx-auto mt-4 sm:mt-6 mb-6 sm:mb-8 bg-blue-900/20 border border-blue-500/30 rounded-lg p-3 sm:p-4 text-left">
                        <h4 className="text-blue-300 text-sm sm:text-base font-medium mb-2 sm:mb-3 flex items-center gap-2">
                            <svg className="w-4 h-4 sm:w-5 sm:h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            Team Requirements
                        </h4>
                        <ul className="space-y-1.5 sm:space-y-2 text-xs sm:text-sm text-gray-300">
                            <li className="flex items-start gap-2">
                                <span className="text-green-400 mt-0.5 flex-shrink-0">&#x2713;</span>
                                <span><strong className="text-white">3 Main Drivers</strong> (required)</span>
                            </li>
                            <li className="flex items-start gap-2">
                                <span className="text-purple-400 mt-0.5 flex-shrink-0">+</span>
                                <span><strong className="text-white">1 Reserve Driver</strong> (optional, 4th driver)</span>
                            </li>
                            <li className="flex items-start gap-2">
                                <span className="text-blue-400 mt-0.5 flex-shrink-0">&#x2713;</span>
                                <span><strong className="text-white">1 Constructor</strong> (team)</span>
                            </li>
                        </ul>
                    </div>

                    <button 
                        onClick={onNavigateToMarket}
                        className="bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white px-6 sm:px-8 py-2.5 sm:py-3 text-sm sm:text-base rounded-lg font-medium transition-all duration-200 shadow-lg hover:shadow-xl"
                    >
                        Go to Driver Market
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="bg-gradient-to-br from-gray-800/40 to-gray-900/40 border border-gray-700/50 backdrop-blur-sm rounded-xl sm:rounded-2xl p-4 sm:p-6 lg:p-8">
            <div className="space-y-4 sm:space-y-6">
                <LeagueStats
                    budgetRemaining={userTeam.budget_remaining}
                    teamValue={teamValue}
                    totalPoints={userTeam.total_points}
                />

                <TeamDisplay
                    drivers={selectedDrivers}
                    constructor={selectedConstructor}
                />

                <div className="mt-4 sm:mt-6 pt-4 sm:pt-6 border-t border-gray-700/50">
                    <button 
                        onClick={onNavigateToMarket}
                        className="hover:cursor-pointer w-full bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white px-4 sm:px-6 py-3 sm:py-4 text-sm sm:text-base rounded-lg font-medium transition-all duration-200 flex items-center justify-center gap-2"
                    >
                        <svg className="w-4 h-4 sm:w-5 sm:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                        </svg>
                        <span className="hidden sm:inline">Driver/Constructor Market</span>
                        <span className="sm:hidden">Market</span>
                    </button>
                </div>

                <div className="mt-6 sm:mt-8 pt-6 sm:pt-8 border-t border-gray-700/50">
                    <h3 className="text-lg sm:text-xl font-bold text-white mb-3 sm:mb-4">Race Weekend Performance</h3>
                    <div className="text-center py-6 sm:py-8 bg-gray-800/30 rounded-lg">
                        <p className="text-gray-400 text-sm sm:text-base">Performance history coming soon...</p>
                        <p className="text-gray-500 text-xs sm:text-sm mt-2">Track your points across all race weekends</p>
                    </div>
                </div>
            </div>
        </div>
    );
};
