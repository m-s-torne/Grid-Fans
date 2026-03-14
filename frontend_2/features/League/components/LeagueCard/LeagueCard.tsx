interface LeagueCardProps {
  id: number;
  name: string;
  description?: string | null;
  current_participants: number;
  join_code: string;
  onClick: (leagueId: number) => void;
}

export const LeagueCard = ({
  id,
  name,
  description,
  current_participants,
  join_code,
  onClick
}: LeagueCardProps) => {
  return (
    <div 
      onClick={() => onClick(id)}
      className="group relative overflow-hidden rounded-xl bg-gradient-to-r from-purple-600/10 to-blue-600/10 border border-purple-500/30 backdrop-blur-sm p-4 sm:p-5 lg:p-6 cursor-pointer transition-all duration-300 hover:scale-102 hover:border-purple-400/50 hover:shadow-xl hover:shadow-purple-500/20"
    >
      <div className="absolute inset-0 bg-gradient-to-r from-purple-600/5 to-blue-600/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
      
      <div className="relative z-10">
        <div className="flex flex-col sm:flex-row justify-between items-start gap-3 sm:gap-4 mb-3 sm:mb-4">
          <div className="flex-1 min-w-0">
            <h3 className="text-lg sm:text-xl font-bold text-white mb-1 sm:mb-2 group-hover:text-purple-300 transition-colors duration-300">
              {name}
            </h3>
            {description && (
              <p className="text-gray-300 text-xs sm:text-sm leading-relaxed line-clamp-2">
                {description}
              </p>
            )}
          </div>
          <div className="flex items-center bg-purple-600/20 text-purple-300 px-2 sm:px-3 py-1 rounded-full text-xs sm:text-sm font-medium border border-purple-500/30 flex-shrink-0">
            <svg className="w-3 h-3 sm:w-4 sm:h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            <span className="whitespace-nowrap">{current_participants} members</span>
          </div>
        </div>
        
        <div className="flex items-center justify-end text-xs sm:text-sm">
          <div className="flex items-center text-blue-400">
            <svg className="w-3 h-3 sm:w-4 sm:h-4 mr-1 sm:mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v-2l-4.257-2.257A6 6 0 0111 7.5h3.5z" />
            </svg>
            <span className="truncate">Code: {join_code}</span>
          </div>
        </div>
      </div>
    </div>
  );
};
