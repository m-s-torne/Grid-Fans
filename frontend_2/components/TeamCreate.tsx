'use client';

import { useTeamBuilderContext } from "@/lib/contexts/TeamBuilderContext";
import { formatCurrencyPrecise } from "@/lib/utils/currencyFormat";

export const TeamCreate = () => {
    const { 
        selectedDrivers, 
        selectedConstructor,
        handleDriverSelect, 
        handleConstructorSelect 
    } = useTeamBuilderContext();

    return (
        <div className="grid md:grid-cols-2 gap-6">
            <div>
                <h3 className="text-lg font-semibold text-gray-300 mb-3">
                    Drivers ({selectedDrivers.length}/3)
                </h3>
                <div className="space-y-2">
                    {selectedDrivers.map((driver) => (
                        <div 
                            key={driver.id}
                            className="flex items-center border gap-3 p-3 rounded-lg group"
                            style={{
                                backgroundColor: `${driver.driver_color}70`,
                                borderColor: `${driver.driver_color}90`
                            }}
                        >
                            <img 
                                src={driver.headshot_url} 
                                alt={driver.full_name}
                                className="w-12 h-12 rounded-full object-cover object-top"
                            />
                            <div className="flex-1">
                                <p className="text-white font-medium">{driver.full_name}</p>
                                <p className="text-gray-100 text-sm">{driver.team_name}</p>
                            </div>
                            <div className="text-right mr-3">
                                <p className="text-gray-100 text-sm font-medium">
                                    {formatCurrencyPrecise(driver.fantasy_stats!.price)}
                                </p>
                            </div>
                            <button
                                onClick={() => handleDriverSelect(driver)}
                                className="p-1 rounded-md bg-red-600/20 hover:bg-red-600/40 border border-red-500/30 hover:border-red-500/60 transition-all duration-150 opacity-0 group-hover:opacity-100"
                                title="Remove driver"
                            >
                                <svg 
                                    className="w-4 h-4 text-red-400 hover:text-red-300" 
                                    fill="none" 
                                    stroke="currentColor" 
                                    viewBox="0 0 24 24"
                                >
                                    <path 
                                        strokeLinecap="round" 
                                        strokeLinejoin="round" 
                                        strokeWidth={2} 
                                        d="M6 18L18 6M6 6l12 12" 
                                    />
                                </svg>
                            </button>
                        </div>
                    ))}
                    {Array.from({ length: 3 - selectedDrivers.length }).map((_, index) => (
                        <div 
                            key={`empty-${index}`}
                            className="flex items-center justify-center p-3 border-2 border-dashed border-gray-600 rounded-lg"
                        >
                            <p className="text-gray-500">Select a driver</p>
                        </div>
                    ))}
                </div>
            </div>
            <div>
                <h3 className="text-lg font-semibold text-gray-300 mb-3">
                    Team ({selectedConstructor ? 1 : 0}/1)
                </h3>
                {selectedConstructor ? (
                    <div 
                        className="p-4 border rounded-lg group"
                        style={{
                            backgroundColor: `${selectedConstructor.team_color}70`,
                            borderColor: `${selectedConstructor.team_color}90`
                        }}
                    >
                        <div className="flex items-center justify-between mb-2">
                            <img 
                                src={`/teams/${selectedConstructor.team_name.toLowerCase().replace(/\s/g, "")}.svg`}
                                alt={`${selectedConstructor.team_name}`}
                                className="max-w-[10%]"
                            />
                            <button
                                onClick={() => handleConstructorSelect(selectedConstructor)}
                                className="p-1 rounded-md bg-red-600/20 hover:bg-red-600/40 border border-red-500/30 hover:border-red-500/60 transition-all duration-150 opacity-0 group-hover:opacity-100"
                                title="Remove team"
                            >
                                <svg 
                                    className="w-4 h-4 text-red-400 hover:text-red-300" 
                                    fill="none" 
                                    stroke="currentColor" 
                                    viewBox="0 0 24 24"
                                >
                                    <path 
                                        strokeLinecap="round" 
                                        strokeLinejoin="round" 
                                        strokeWidth={2} 
                                        d="M6 18L18 6M6 6l12 12" 
                                    />
                                </svg>
                            </button>
                        </div>
                        <p className="text-white font-medium">{selectedConstructor.team_name}</p>
                        <p className="text-gray-100 text-sm">
                            {selectedConstructor.season_results?.points || 0} points
                        </p>
                    </div>
                ) : (
                    <div className="flex items-center justify-center p-4 border-2 border-dashed border-gray-600 rounded-lg">
                        <p className="text-gray-500">Select a team</p>
                    </div>
                )}
            </div>
        </div>
    )
}
