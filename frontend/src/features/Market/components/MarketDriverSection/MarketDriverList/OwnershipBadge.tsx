import type { DriverOwnership } from '@/features/Market/types/marketTypes';

interface OwnershipBadgeProps {
  ownership: DriverOwnership | null;
  currentUserId: number;
  ownerName?: string;
  isReserve?: boolean;
  compact?: boolean;
}

export const OwnershipBadge = ({ 
  ownership, 
  currentUserId, 
  ownerName,
  isReserve = false,
  compact = false 
}: OwnershipBadgeProps) => {
  // Free Agent
  if (!ownership || ownership.owner_id === null) {
    return (
      <div className={`inline-flex items-center gap-1 px-2 py-1 rounded-full bg-green-500/20 border border-green-500 ${compact ? 'text-[10px]' : 'text-xs'}`}>
        <svg className={`${compact ? 'w-3 h-3' : 'w-4 h-4'} text-green-400`} fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
        </svg>
        <span className="text-green-300 font-medium">Free</span>
      </div>
    );
  }

  // Owned by current user
  if (ownership.owner_id === currentUserId) {
    if (ownership.is_listed_for_sale) {
      return (
        <div className={`inline-flex items-center gap-1 px-2 py-1 rounded-full bg-yellow-500/20 border border-yellow-500 ${compact ? 'text-[10px]' : 'text-xs'}`}>
          <svg className={`${compact ? 'w-3 h-3' : 'w-4 h-4'} text-yellow-400`} fill="currentColor" viewBox="0 0 20 20">
            <path d="M8.433 7.418c.155-.103.346-.196.567-.267v1.698a2.305 2.305 0 01-.567-.267C8.07 8.34 8 8.114 8 8c0-.114.07-.34.433-.582zM11 12.849v-1.698c.22.071.412.164.567.267.364.243.433.468.433.582 0 .114-.07.34-.433.582a2.305 2.305 0 01-.567.267z" />
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v.092a4.535 4.535 0 00-1.676.662C6.602 6.234 6 7.009 6 8c0 .99.602 1.765 1.324 2.246.48.32 1.054.545 1.676.662v1.941c-.391-.127-.68-.317-.843-.504a1 1 0 10-1.51 1.31c.562.649 1.413 1.076 2.353 1.253V15a1 1 0 102 0v-.092a4.535 4.535 0 001.676-.662C13.398 13.766 14 12.991 14 12c0-.99-.602-1.765-1.324-2.246A4.535 4.535 0 0011 9.092V7.151c.391.127.68.317.843.504a1 1 0 101.511-1.31c-.563-.649-1.413-1.076-2.354-1.253V5z" clipRule="evenodd" />
          </svg>
          <span className="text-yellow-300 font-medium">For Sale</span>
        </div>
      );
    }
    
    if (isReserve) {
      return (
        <div className={`inline-flex items-center gap-1 px-2 py-1 rounded-full bg-purple-500/20 border border-purple-500 ${compact ? 'text-[10px]' : 'text-xs'}`}>
          <svg className={`${compact ? 'w-3 h-3' : 'w-4 h-4'} text-purple-400`} fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clipRule="evenodd" />
          </svg>
          <span className="text-purple-300 font-medium">Reserve</span>
        </div>
      );
    }
    
    return (
      <div className={`inline-flex items-center gap-1 px-2 py-1 rounded-full bg-blue-500/20 border border-blue-500 ${compact ? 'text-[10px]' : 'text-xs'}`}>
        <svg className={`${compact ? 'w-3 h-3' : 'w-4 h-4'} text-blue-400`} fill="currentColor" viewBox="0 0 20 20">
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
        </svg>
        <span className="text-blue-300 font-medium">Mine</span>
      </div>
    );
  }

  // Owned by another user
  const isLocked = ownership.locked_until && new Date(ownership.locked_until) > new Date();
  
  if (isLocked) {
    return (
      <div className={`inline-flex items-center gap-1 px-2 py-1 rounded-full bg-red-500/20 border border-red-500 ${compact ? 'text-[10px]' : 'text-xs'}`}>
        <svg className={`${compact ? 'w-3 h-3' : 'w-4 h-4'} text-red-400`} fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clipRule="evenodd" />
        </svg>
        <span className="text-red-300 font-medium">Locked</span>
      </div>
    );
  }

  if (ownership.is_listed_for_sale) {
    return (
      <div className={`inline-flex items-center gap-1 px-2 py-1 rounded-full bg-yellow-500/20 border border-yellow-500 ${compact ? 'text-[10px]' : 'text-xs'}`}>
        <svg className={`${compact ? 'w-3 h-3' : 'w-4 h-4'} text-yellow-400`} fill="currentColor" viewBox="0 0 20 20">
          <path d="M8.433 7.418c.155-.103.346-.196.567-.267v1.698a2.305 2.305 0 01-.567-.267C8.07 8.34 8 8.114 8 8c0-.114.07-.34.433-.582zM11 12.849v-1.698c.22.071.412.164.567.267.364.243.433.468.433.582 0 .114-.07.34-.433.582a2.305 2.305 0 01-.567.267z" />
          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v.092a4.535 4.535 0 00-1.676.662C6.602 6.234 6 7.009 6 8c0 .99.602 1.765 1.324 2.246.48.32 1.054.545 1.676.662v1.941c-.391-.127-.68-.317-.843-.504a1 1 0 10-1.51 1.31c.562.649 1.413 1.076 2.353 1.253V15a1 1 0 102 0v-.092a4.535 4.535 0 001.676-.662C13.398 13.766 14 12.991 14 12c0-.99-.602-1.765-1.324-2.246A4.535 4.535 0 0011 9.092V7.151c.391.127.68.317.843.504a1 1 0 101.511-1.31c-.563-.649-1.413-1.076-2.354-1.253V5z" clipRule="evenodd" />
        </svg>
        <span className="text-yellow-300 font-medium">
          {compact ? 'Sale' : ownerName ? `${ownerName}'s` : 'For Sale'}
        </span>
      </div>
    );
  }

  return (
    <div className={`inline-flex items-center gap-1 px-2 py-1 rounded-full bg-gray-500/20 border border-gray-500 ${compact ? 'text-[10px]' : 'text-xs'}`}>
      <svg className={`${compact ? 'w-3 h-3' : 'w-4 h-4'} text-gray-400`} fill="currentColor" viewBox="0 0 20 20">
        <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
      </svg>
      <span className="text-gray-300 font-medium">
        {compact ? 'Owned' : ownerName || 'Owned'}
      </span>
    </div>
  );
};
