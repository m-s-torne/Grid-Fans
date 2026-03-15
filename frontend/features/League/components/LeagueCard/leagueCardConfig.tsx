export type ActionCardVariant = 'create' | 'join';
export const cardConfig = {
  create: {
    gradient: 'from-red-600/20 to-red-800/20',
    border: 'border-red-500/30',
    hoverBorder: 'hover:border-red-400/50',
    hoverShadow: 'hover:shadow-red-500/20',
    bgGradient: 'from-red-600/10',
    iconBg: 'bg-red-600/20',
    iconBorder: 'border-red-500/30',
    iconHoverBg: 'group-hover:bg-red-600/30',
    iconColor: 'text-red-400',
    textColor: 'text-red-400',
    textHoverColor: 'group-hover:text-red-300',
    bgIcon: 'text-red-500',
    icon: (
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
    ),
    actionIcon: (
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
    ),
    title: 'Create League',
    description: 'Start your own fantasy league and invite friends to compete. Immerse yourself in a realistic driver market.',
    actionText: 'Get Started',
  },
  join: {
    gradient: 'from-blue-600/20 to-blue-800/20',
    border: 'border-blue-500/30',
    hoverBorder: 'hover:border-blue-400/50',
    hoverShadow: 'hover:shadow-blue-500/20',
    bgGradient: 'from-blue-600/10',
    iconBg: 'bg-blue-600/20',
    iconBorder: 'border-blue-500/30',
    iconHoverBg: 'group-hover:bg-blue-600/30',
    iconColor: 'text-blue-400',
    textColor: 'text-blue-400',
    textHoverColor: 'group-hover:text-blue-300',
    bgIcon: 'text-blue-500',
    icon: (
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
    ),
    actionIcon: (
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
    ),
    title: 'Join League',
    description: 'Enter a league code or search for public leagues to join the competition and test your F1 knowledge.',
    actionText: 'Find Leagues',
  },
};
