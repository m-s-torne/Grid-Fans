import { cardConfig, type ActionCardVariant } from '@/features/League/components/LeagueCard/leagueCardConfig';
interface LeagueActionCardProps {
  variant: ActionCardVariant;
  onClick: () => void;
}

export const LeagueActionCard = ({ variant, onClick }: LeagueActionCardProps) => {
  const config = cardConfig[variant];

  return (
    <div 
      onClick={onClick}
      className={`group relative overflow-hidden rounded-xl sm:rounded-2xl bg-gradient-to-br ${config.gradient} border ${config.border} backdrop-blur-sm p-6 sm:p-7 lg:p-8 cursor-pointer transition-all duration-300 hover:scale-105 ${config.hoverBorder} hover:shadow-2xl ${config.hoverShadow}`}
    >
      <div className={`absolute inset-0 bg-gradient-to-br ${config.bgGradient} to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300`} />
      
      <div className="relative z-10">
        <div className={`flex items-center justify-center w-12 h-12 sm:w-14 sm:h-14 lg:w-16 lg:h-16 rounded-full ${config.iconBg} border ${config.iconBorder} mb-4 sm:mb-5 lg:mb-6 ${config.iconHoverBg} transition-colors duration-300`}>
          <svg className={`w-6 h-6 sm:w-7 sm:h-7 lg:w-8 lg:h-8 ${config.iconColor}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
            {config.icon}
          </svg>
        </div>
        
        <h3 className="text-xl sm:text-2xl font-bold text-white mb-3 sm:mb-4">
          {config.title}
        </h3>
        
        <p className="text-sm sm:text-base text-gray-300 mb-4 sm:mb-5 lg:mb-6 leading-relaxed">
          {config.description}
        </p>
        
        <div className={`flex items-center ${config.textColor} text-sm sm:text-base font-medium ${config.textHoverColor} transition-colors duration-300`}>
          <span>{config.actionText}</span>
          <svg className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            {config.actionIcon}
          </svg>
        </div>
      </div>
      
      <div className="absolute top-3 right-3 sm:top-4 sm:right-4 opacity-10 group-hover:opacity-20 transition-opacity duration-300">
        <svg className={`w-20 h-20 sm:w-24 sm:h-24 ${config.bgIcon}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d={variant === 'create' ? 'M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z' : 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z'} />
        </svg>
      </div>
    </div>
  );
};
