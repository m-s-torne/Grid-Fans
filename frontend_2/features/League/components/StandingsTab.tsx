import type { StandingsTabProps } from '@/features/League/types/leagueTypes';

export const StandingsTab = ({
    participants,
    totalParticipants,
    isLoading
}: StandingsTabProps) => {
    return (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 sm:gap-8">
            <div className="bg-gradient-to-br from-gray-800/40 to-gray-900/40 border border-gray-700/50 backdrop-blur-sm rounded-xl sm:rounded-2xl p-4 sm:p-6 lg:p-8">
                <h2 className="text-xl sm:text-2xl font-bold text-white mb-4 sm:mb-6">Participants</h2>
                
                {isLoading ? (
                    <div className="flex items-center justify-center py-6 sm:py-8">
                        <div className="animate-spin rounded-full h-6 w-6 sm:h-8 sm:w-8 border-b-2 border-blue-400"></div>
                    </div>
                ) : participants.length > 0 ? (
                    <div className="space-y-2 sm:space-y-3">
                        {participants.map((participant) => (
                            <div 
                                key={participant.user_id}
                                className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 sm:gap-0 p-3 sm:p-4 bg-gray-700/30 rounded-lg border border-gray-600/30"
                            >
                                <div className="flex items-center gap-2 sm:gap-3">
                                    <div className="w-8 h-8 sm:w-10 sm:h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white text-sm sm:text-base font-bold flex-shrink-0">
                                        {participant.user_name.charAt(0).toUpperCase()}
                                    </div>
                                    <div className="min-w-0">
                                        <p className="text-white text-sm sm:text-base font-medium truncate">{participant.user_name}</p>
                                        <p className="text-gray-400 text-xs sm:text-sm truncate">{participant.email}</p>
                                    </div>
                                </div>
                                <div className="flex items-center gap-2 ml-10 sm:ml-0">
                                    {participant.is_admin && (
                                        <span className="bg-yellow-600/20 text-yellow-300 px-2 sm:px-3 py-0.5 sm:py-1 rounded-full text-[10px] sm:text-xs font-medium border border-yellow-500/30">
                                            Admin
                                        </span>
                                    )}
                                    <span className="text-gray-400 text-[10px] sm:text-xs">
                                        Joined {new Date(participant.joined_at).toLocaleDateString()}
                                    </span>
                                </div>
                            </div>
                        ))}
                        
                        <div className="mt-4 sm:mt-6 pt-3 sm:pt-4 border-t border-gray-600/30">
                            <p className="text-gray-400 text-xs sm:text-sm">
                                Total: {totalParticipants} participants
                            </p>
                        </div>
                    </div>
                ) : (
                    <p className="text-gray-400 text-sm sm:text-base">No participants found</p>
                )}
            </div>
            
            <div className="bg-gradient-to-br from-gray-800/40 to-gray-900/40 border border-gray-700/50 backdrop-blur-sm rounded-xl sm:rounded-2xl p-4 sm:p-6 lg:p-8">
                <h2 className="text-xl sm:text-2xl font-bold text-white mb-3 sm:mb-4">Leaderboard</h2>
                <p className="text-gray-400 text-sm sm:text-base">Leaderboard coming soon...</p>
            </div>
        </div>
    );
};
