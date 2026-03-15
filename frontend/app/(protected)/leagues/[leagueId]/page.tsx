'use client';

import { useRouter, useParams } from 'next/navigation';
import { useLeagueDetail, useLeagueParticipants } from '@/features/League/hooks';
import { LoadingSpinner, LoadingError } from '@/components';
import { LeagueHeader, LineupTab, StandingsTab } from '@/features/League/components';
import { LeaveLeagueModal } from '@/features/League/components/modals';

export default function LeagueDetailPage() {
    const params = useParams<{ leagueId: string }>();
    const leagueId = params.leagueId;
    const {
        league,
        isLoading,
        error,
        userTeam,
        teamLoading,
        allDrivers,
        allTeams,
        selectedDrivers,
        selectedConstructor,
        teamValue,
        activeTab,
        setActiveTab,
        showLeaveModal,
        setShowLeaveModal,
        handleLeaveLeague,
        isLeavingLeague,
        navigateToMarket,
    } = useLeagueDetail(leagueId!);
    
    const router = useRouter();
    
    const { data: participantsData, isLoading: participantsLoading } = useLeagueParticipants(parseInt(leagueId!));

    if (isLoading) {
        return (
            <div className="max-w-6xl mx-auto">
                <LoadingSpinner message={"Loading league details"}/>
            </div>
        );
    }

    if (error || !league) {
        return (
            <div className="p-6">
                <div className="max-w-6xl mx-auto">
                    <LoadingError error={"Error loading league"} errorMessage={"League not found or access denied"}/>
                </div>
            </div>
        );
    }

    return (
        <div className="p-4 sm:p-6 lg:p-8">
            <div className="max-w-6xl mx-auto">
                {/* Back to Leagues button */}
                <button
                    onClick={() => router.push("/leagues")}
                    className="flex items-center text-gray-400 hover:text-white mb-3 sm:mb-4 transition-colors cursor-pointer"
                >
                    <svg className="w-4 h-4 sm:w-5 sm:h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                    </svg>
                    <span className="text-sm sm:text-base">Back to Leagues</span>
                </button>

                <LeagueHeader
                    name={league.name}
                    description={league.description}
                    joinCode={league.join_code}
                    currentParticipants={league.current_participants || 0}
                    activeTab={activeTab}
                    onTabChange={setActiveTab}
                />

                {/* Tab Content */}
                {activeTab === 'lineup' ? (
                    <LineupTab
                        userTeam={userTeam}
                        teamLoading={teamLoading}
                        allDriversLoaded={!!allDrivers}
                        allTeamsLoaded={!!allTeams}
                        selectedDrivers={selectedDrivers}
                        selectedConstructor={selectedConstructor}
                        teamValue={teamValue}
                        onNavigateToMarket={navigateToMarket}
                    />
                ) : (
                    <StandingsTab
                        participants={participantsData?.participants || []}
                        totalParticipants={participantsData?.total_participants || 0}
                        isLoading={participantsLoading}
                    />
                )}

                {/* Leave League Button - Bottom of page */}
                <div className="mt-6 sm:mt-8 flex justify-center">
                    <button 
                        onClick={() => setShowLeaveModal(true)}
                        disabled={isLeavingLeague}
                        className="hover:cursor-pointer bg-gradient-to-r from-red-600/20 to-red-700/20 hover:from-red-600/30 hover:to-red-700/30 disabled:from-red-400/10 disabled:to-red-500/10 text-red-400 hover:text-red-300 disabled:text-red-500 px-4 sm:px-6 py-2 sm:py-3 text-sm sm:text-base rounded-lg font-medium transition-all duration-200 border border-red-500/30 hover:border-red-500/50"
                    >
                        {isLeavingLeague ? 'Leaving...' : 'Leave League'}
                    </button>
                </div>
            </div>

            {/* Leave League Confirmation Modal */}
            {showLeaveModal && (
                <LeaveLeagueModal
                    leagueName={league.name}
                    isLeaving={isLeavingLeague}
                    onConfirm={handleLeaveLeague}
                    onCancel={() => setShowLeaveModal(false)}
                />
            )}
        </div>
    );
}
