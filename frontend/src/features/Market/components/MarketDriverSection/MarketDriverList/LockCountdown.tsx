import { useLockCountDown } from '@/features/Market/hooks/useLockCountdown';

interface LockCountdownProps {
  lockedUntil: string | null;
  compact?: boolean;
}

export const LockCountdown = ({ lockedUntil, compact = false }: LockCountdownProps) => {
  const { timeRemaining, progress, color, colorClasses } = useLockCountDown(lockedUntil)
  
  if (!lockedUntil || !timeRemaining) {
        return null;
  }

  if (compact) {
    return (
      <div className={`inline-flex items-center gap-1 px-2 py-1 rounded-full border text-[10px] font-medium ${colorClasses[color]}`}>
        🔒 {timeRemaining}
      </div>
    );
  }

  return (
    <div className={`inline-flex flex-col gap-1 px-3 py-2 rounded-lg border ${colorClasses[color]}`}>
      <div className="flex items-center gap-2">
        <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clipRule="evenodd" />
        </svg>
        <span className="text-xs font-bold">{timeRemaining}</span>
      </div>
      <div className="w-full bg-gray-700/50 rounded-full h-1.5 overflow-hidden">
        <div 
          className={`h-full transition-all duration-1000 ${
            color === 'red' ? 'bg-red-500' : 
            color === 'yellow' ? 'bg-yellow-500' : 
            'bg-green-500'
          }`}
          style={{ width: `${progress}%` }}
        />
      </div>
    </div>
  );
};
