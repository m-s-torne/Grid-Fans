import type { TeamDisplayProps, LineupDriver } from '@/features/League/types/leagueTypes';
import { formatCurrencyPrecise } from '@/lib/utils';

export const TeamDisplay = ({ drivers, constructor: team }: TeamDisplayProps) => {
    const validDrivers = drivers.filter(Boolean) as LineupDriver[];
    const mainDrivers = validDrivers.slice(0, 3);
    const reserveDriver = validDrivers[3];

    const getLastName = (fullName: string) => {
        const nameParts = fullName.trim().split(' ');
        const lastName = nameParts[nameParts.length - 1];
        return lastName.substring(0, 3).toUpperCase();
    };

    return (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
            {/* Drivers Section */}
            <section>
                <div className="mb-4">
                    <h3 className="text-base sm:text-lg font-semibold text-gray-300 mb-2 sm:mb-3 flex items-center gap-2">
                        Main Drivers
                        <span className="text-xs text-gray-500 bg-gray-700/50 px-2 py-0.5 rounded-full">
                            {mainDrivers.length}/3
                        </span>
                    </h3>
                    <div className="space-y-2">
                        {mainDrivers.map((driver) => (
                            <div 
                                key={driver.id}
                                className="flex items-center border gap-2 sm:gap-3 p-2 sm:p-3 rounded-lg"
                                style={{
                                    backgroundColor: `${driver.driver_color}70`,
                                    borderColor: `${driver.driver_color}90`
                                }}
                            >
                                <img 
                                    src={driver.headshot_url} 
                                    alt={driver.full_name}
                                    className="w-10 h-10 sm:w-12 sm:h-12 rounded-full object-cover object-top flex-shrink-0"
                                />
                                <div className="flex-1 min-w-0">
                                    <p className="text-white text-xs sm:text-base font-medium truncate">
                                        <span className="sm:hidden">{getLastName(driver.full_name)}</span>
                                        <span className="hidden sm:inline">{driver.full_name}</span>
                                    </p>
                                    <p className="text-gray-100 text-[10px] sm:text-sm truncate">{driver.team_name}</p>
                                </div>
                                {driver.ownership?.acquisition_price && (
                                    <div className="text-right flex-shrink-0">
                                        <p className="text-white text-xs sm:text-sm font-medium">
                                            {formatCurrencyPrecise(driver.ownership.acquisition_price)}
                                        </p>
                                    </div>
                                )}
                            </div>
                        ))}
                        {mainDrivers.length < 3 && Array.from({ length: 3 - mainDrivers.length }).map((_, i) => (
                            <div 
                                key={`empty-main-${i}`}
                                className="flex items-center justify-center border-2 border-dashed border-gray-600/50 rounded-lg p-2 sm:p-3 h-14 sm:h-[72px]"
                            >
                                <p className="text-gray-500 text-xs sm:text-sm">Empty slot</p>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Reserve Driver */}
                <div>
                    <h3 className="text-base sm:text-lg font-semibold text-gray-300 mb-2 sm:mb-3 flex items-center gap-2">
                        Reserve Driver
                        <span className="text-xs text-purple-400 bg-purple-900/30 px-2 py-0.5 rounded-full border border-purple-500/30">
                            Optional
                        </span>
                    </h3>
                    {reserveDriver ? (
                        <div 
                            className="flex items-center border gap-2 sm:gap-3 p-2 sm:p-3 rounded-lg relative"
                            style={{
                                backgroundColor: `${reserveDriver.driver_color}70`,
                                borderColor: `${reserveDriver.driver_color}90`
                            }}
                        >
                            <img 
                                src={reserveDriver.headshot_url} 
                                alt={reserveDriver.full_name}
                                className="w-10 h-10 sm:w-12 sm:h-12 rounded-full object-cover object-top flex-shrink-0"
                            />
                            <div className="flex-1 min-w-0">
                                <div className="flex items-center gap-1.5 mb-0.5">
                                    <p className="text-white text-xs sm:text-base font-medium truncate">
                                        <span className="sm:hidden">{getLastName(reserveDriver.full_name)}</span>
                                        <span className="hidden sm:inline">{reserveDriver.full_name}</span>
                                    </p>
                                    <span className="bg-purple-600/90 text-white text-[9px] sm:text-[10px] font-bold px-1.5 py-0.5 rounded-full border border-purple-400/50 flex-shrink-0">
                                        RESERVE
                                    </span>
                                </div>
                                <p className="text-gray-100 text-[10px] sm:text-sm truncate">{reserveDriver.team_name}</p>
                            </div>
                            {reserveDriver.ownership?.acquisition_price && (
                                <div className="text-right flex-shrink-0">
                                    <p className="text-white text-xs sm:text-sm font-medium">
                                        {formatCurrencyPrecise(reserveDriver.ownership.acquisition_price)}
                                    </p>
                                </div>
                            )}
                        </div>
                    ) : (
                        <div className="flex flex-col items-center justify-center border-2 border-dashed border-purple-600/30 bg-purple-900/10 rounded-lg p-3 sm:p-4 h-14 sm:h-[72px]">
                            <p className="text-purple-400/70 text-xs sm:text-sm">No reserve driver</p>
                            <p className="text-purple-500/50 text-[10px] sm:text-xs mt-0.5 sm:mt-1">4th driver slot available</p>
                        </div>
                    )}
                </div>
            </section>

            {/* Constructor Section */}
            <section>
                <h3 className="text-base sm:text-lg font-semibold text-gray-300 mb-2 sm:mb-3">
                    Constructor
                </h3>
                {team ? (
                    <div 
                        className="p-3 sm:p-4 border rounded-lg"
                        style={{
                            backgroundColor: `${team.team_color}70`,
                            borderColor: `${team.team_color}90`
                        }}
                    >
                        <div className="flex items-center justify-between mb-2">
                            <img 
                                src={`/teams/${team.team_name.toLowerCase().replace(/\s/g, "")}.svg`}
                                alt={`${team.team_name}`}
                                className="max-w-[15%] sm:max-w-[10%]"
                            />
                        </div>
                        <p className="text-white text-sm sm:text-base font-medium">{team.team_name}</p>
                        <p className="text-gray-100 text-xs sm:text-sm">
                            {team.season_results?.points || 0} points
                        </p>
                    </div>
                ) : (
                    <div className="flex items-center justify-center p-3 sm:p-4 border-2 border-dashed border-gray-600 rounded-lg h-24 sm:h-auto">
                        <p className="text-gray-500 text-sm">Select a team</p>
                    </div>
                )}
            </section>
        </div>
    );
};
