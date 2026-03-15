'use client';

import { useRouter } from 'next/navigation';
import { useLeagues } from '@/lib/contexts/LeaguesContext';
import { useLeagueModals } from '@/features/League/hooks';
import { CreateLeagueModal } from '@/features/League/components/modals';
import { JoinLeagueModal } from '@/features/League/components/modals';
import { LeagueCard, LeagueActionCard } from '@/features/League/components';

export default function LeaguesPage() {
    const router = useRouter();
    const { leagues, isLoading, error } = useLeagues();
    const { 
        showCreateModal, 
        showJoinModal, 
        openCreateModal, 
        closeCreateModal, 
        openJoinModal, 
        closeJoinModal 
    } = useLeagueModals();

    const handleLeagueClick = (leagueId: number) => {
        router.push(`/leagues/${leagueId}`);
    };

    return (
        <div className="p-4 sm:p-6 lg:p-8">
            <div className="max-w-6xl mx-auto">
                {/* Header */}
                <div className="text-center mb-8 sm:mb-10 lg:mb-12">
                    <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold text-white mb-3 sm:mb-4 px-4">
                        F1 Fantasy Leagues
                    </h1>
                    <p className="text-gray-300 text-sm sm:text-base lg:text-lg px-4">
                        Create or join leagues to compete with friends and other F1 fans
                    </p>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6 lg:gap-8 mb-8 sm:mb-10 lg:mb-12">
                    <LeagueActionCard 
                        variant="create" 
                        onClick={openCreateModal} 
                    />
                    
                    <LeagueActionCard 
                        variant="join" 
                        onClick={openJoinModal} 
                    />
                </div>

                {/* My Leagues Section */}
                <div className="rounded-2xl bg-black/30 backdrop-blur-sm border border-white/20 p-4 sm:p-6 lg:p-8">
                    <h2 className="text-xl sm:text-2xl font-bold text-white mb-4 sm:mb-6 flex items-center">
                        <svg className="w-5 h-5 sm:w-6 sm:h-6 mr-2 sm:mr-3 text-yellow-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
                        </svg>
                        My Leagues
                    </h2>
                    
                    {isLoading ? (
                        <div className="text-center py-8 sm:py-12">
                            <div className="animate-spin rounded-full h-12 w-12 sm:h-16 sm:w-16 border-b-2 border-red-500 mx-auto mb-4"></div>
                            <p className="text-sm sm:text-base lg:text-lg text-gray-400">Loading your leagues...</p>
                        </div>
                    ) : error ? (
                        <div className="text-center py-8 sm:py-12">
                            <svg className="w-12 h-12 sm:w-16 sm:h-16 text-red-500 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            <p className="text-base sm:text-lg text-red-400">Error loading leagues</p>
                            <p className="text-sm sm:text-base text-gray-500 mt-2">{error.message}</p>
                        </div>
                    ) : leagues.length === 0 ? (
                        <div className="text-center py-8 sm:py-12">
                            <svg className="w-12 h-12 sm:w-16 sm:h-16 text-gray-500 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                            </svg>
                            <p className="text-base sm:text-lg text-gray-400">
                                You haven&apos;t joined any leagues yet
                            </p>
                            <p className="text-sm sm:text-base text-gray-500 mt-2">
                                Create or join a league to start competing!
                            </p>
                        </div>
                    ) : (
                        <div className="grid gap-4 sm:gap-6">
                            {leagues.map((league) => (
                                <LeagueCard
                                    key={league.id}
                                    id={league.id}
                                    name={league.name}
                                    description={league.description ?? undefined}
                                    current_participants={league.current_participants}
                                    join_code={league.join_code}
                                    onClick={handleLeagueClick}
                                />
                            ))}
                        </div>
                    )}
                </div>
            </div>

            {/* Modals */}
            <CreateLeagueModal 
                isOpen={showCreateModal} 
                onClose={closeCreateModal} 
            />
            
            <JoinLeagueModal 
                isOpen={showJoinModal} 
                onClose={closeJoinModal} 
            />
        </div>
    );
}
