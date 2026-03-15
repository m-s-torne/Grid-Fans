interface DriverSlotsDisplayProps {
  driverCount: number;
  maxDrivers?: number;
}

export const DriverSlotsDisplay = ({ 
  driverCount, 
  maxDrivers = 4 
}: DriverSlotsDisplayProps) => {
  const mainDrivers = Math.min(driverCount, 3);
  const hasReserve = driverCount === 4;

  return (
    <div className="w-fit bg-gradient-to-br from-blue-600/20 to-blue-700/20 border border-blue-500/50 rounded-lg sm:rounded-xl px-3 sm:px-6 py-2 sm:py-3">
      <p className="text-blue-300 text-xs sm:text-sm font-medium mb-1 sm:mb-2">Your Team</p>
      
      <div className="flex items-center gap-2 sm:gap-3">
        <div className="flex flex-col gap-1">
          <div className="flex items-center gap-1">
            {[1, 2, 3].map((slot) => (
              <div
                key={slot}
                className={`w-2 h-2 sm:w-3 sm:h-3 rounded-full border-2 transition-all ${
                  slot <= mainDrivers
                    ? 'bg-blue-400 border-blue-400 shadow-sm shadow-blue-400/50'
                    : 'bg-transparent border-gray-600'
                }`}
                title={`Main Driver ${slot}${slot <= mainDrivers ? ' (filled)' : ' (empty)'}`}
              />
            ))}
          </div>
          <span className="text-[10px] sm:text-xs text-gray-400 whitespace-nowrap">Main</span>
        </div>

        <div className="w-px h-6 sm:h-8 bg-blue-500/30" />

        <div className="flex flex-col gap-1">
          <div
            className={`w-2 h-2 sm:w-3 sm:h-3 rounded-full border-2 transition-all ${
              hasReserve
                ? 'bg-purple-400 border-purple-400 shadow-sm shadow-purple-400/50'
                : 'bg-transparent border-gray-600'
            }`}
            title={`Reserve Driver${hasReserve ? ' (filled)' : ' (empty)'}`}
          />
          <span className="text-[10px] sm:text-xs text-gray-400 whitespace-nowrap">Reserve</span>
        </div>

        <div className="ml-1 sm:ml-2">
          <p className="text-white text-lg sm:text-2xl font-bold whitespace-nowrap">
            {driverCount}/{maxDrivers}
          </p>
        </div>
      </div>

      {driverCount < 3 && (
        <p className="text-[10px] sm:text-xs text-yellow-400 mt-1 sm:mt-2">
          &#x26A0;&#xFE0F; Add {3 - driverCount} more main driver{3 - driverCount > 1 ? 's' : ''}
        </p>
      )}
      {driverCount === 3 && (
        <p className="text-[10px] sm:text-xs text-blue-300 mt-1 sm:mt-2">
          &#x1F4A1; Add 1 reserve driver (optional)
        </p>
      )}
      {driverCount === 4 && (
        <p className="text-[10px] sm:text-xs text-green-400 mt-1 sm:mt-2 flex items-center gap-1">
          <svg className="w-2 h-2 sm:w-3 sm:h-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
          </svg>
          Team complete!
        </p>
      )}
    </div>
  );
};
