export const DriverSkeleton = () => (
    <div className="p-3 sm:p-4 rounded-lg border border-blue-500 bg-gray-800/50 animate-pulse">
    <div className="flex items-center gap-2 sm:gap-3 mb-2 sm:mb-3">
        <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-full bg-blue-500/30 flex-shrink-0" />
        <div className="flex-1 min-w-0">
        <div className="h-3 sm:h-4 bg-blue-500/30 rounded w-3/4 mb-2" />
        <div className="h-2 sm:h-3 bg-blue-500/30 rounded w-1/2" />
        </div>
    </div>
    <div className="grid grid-cols-3 gap-1 sm:gap-2 mb-2 sm:mb-3">
        <div className="h-10 sm:h-12 bg-blue-500/20 rounded" />
        <div className="h-10 sm:h-12 bg-blue-500/20 rounded" />
        <div className="h-10 sm:h-12 bg-blue-500/20 rounded" />
    </div>
    <div className="h-8 sm:h-10 bg-blue-500/20 rounded" />
    <div className="text-center mt-2 text-[10px] sm:text-xs text-blue-400">
        Swapping drivers...
    </div>
    </div>
);
