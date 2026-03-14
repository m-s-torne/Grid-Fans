'use client';

import { memo } from 'react';
import type { Driver } from '@/features/Market/types/marketTypes';
import { 
    BarChart, 
    Bar, 
    XAxis, 
    YAxis, 
    ResponsiveContainer, 
    Cell, 
    LabelList,
    PieChart,
    Pie
} from 'recharts';

interface DriverStatsChartsProps {
    season_results: NonNullable<Driver['season_results']>;
    fantasy_stats: NonNullable<Driver['fantasy_stats']>;
}

export const DriverStatsCharts = memo(({ season_results, fantasy_stats }: DriverStatsChartsProps) => {
    const achievementsData = [
        { name: 'VICTORIES', value: season_results.victories, color: '#ffd700' },
        { name: 'POLES', value: season_results.poles, color: '#c0c0c0' },
        { name: 'PODIUMS', value: season_results.podiums, color: '#cd7f32' }
    ];

    const avgFinishData = [
        { name: 'AVG FINISH', value: fantasy_stats.avg_finish, color: '#3b82f6' }
    ];

    const overtakeData = [
        { 
            name: '', 
            value: fantasy_stats.overtake_efficiency,
            color: fantasy_stats.overtake_efficiency >= 0.5 ? '#22c55e' : 
                   fantasy_stats.overtake_efficiency >= 0 ? '#f59e0b' : '#ef4444'
        }
    ];

    const availablePointsData = [
        { name: 'Achieved', value: fantasy_stats.available_points_percentatge, color: '#22c55e' },
        { name: 'Missed', value: 100 - fantasy_stats.available_points_percentatge, color: '#6b7280' }
    ];

    const poleWinData = [
        { name: 'Success', value: fantasy_stats.pole_win_conversion, color: '#ffd700' },
        { name: 'Miss', value: 100 - fantasy_stats.pole_win_conversion, color: '#6b7280' }
    ];

    return (
        <div className="flex flex-col gap-4 sm:gap-6 md:gap-10 p-2 sm:p-4 md:p-5">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-3 sm:gap-4 md:gap-6">
                <div className="bg-transparent backdrop-blur-lg border border-white/20 rounded-xl sm:rounded-2xl p-3 sm:p-4">
                    <h4 className="text-[8px] sm:text-[9px] md:text-[10px] font-medium text-white/80 uppercase tracking-wide text-center mb-2 sm:mb-3 md:mb-4">
                        Season Achievements
                    </h4>
                    <div className="h-40 sm:h-48 md:h-60">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={achievementsData} margin={{ top: 5, right: 5, left: 5, bottom: 20 }}>
                                <XAxis 
                                    dataKey="name" 
                                    axisLine={false} 
                                    tickLine={false}
                                    tick={{ fill: '#ffffff80', fontSize: 8 }}
                                    interval={0}
                                />
                                <YAxis hide />
                                <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                                    <LabelList 
                                        dataKey="value" 
                                        position="center" 
                                        fill="#ffffff" 
                                        fontSize={10} 
                                        fontWeight="bold"
                                    />
                                    {achievementsData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={entry.color} />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>
                <div className="bg-transparent backdrop-blur-sm border border-white/20 rounded-xl sm:rounded-2xl p-3 sm:p-4">
                    <h4 className="text-[8px] sm:text-[9px] md:text-[10px] font-medium text-white/80 uppercase tracking-wide text-center mb-2 sm:mb-3 md:mb-4">
                        Average Finish
                    </h4>
                    <div className="h-40 sm:h-48 md:h-60">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={avgFinishData} margin={{ top: 5, right: 5, left: 5, bottom: 10 }}>
                                <XAxis 
                                    dataKey="name" 
                                    axisLine={false} 
                                    tickLine={false}
                                    tick={{ fill: '#ffffff80', fontSize: 8 }}
                                />
                                <YAxis hide domain={[0, 20]} />
                                <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                                    <LabelList 
                                        dataKey="value" 
                                        position="center" 
                                        fill="#ffffff" 
                                        fontSize={12} 
                                        fontWeight="bold"
                                        formatter={((value: number | string | null | undefined) => typeof value === 'number' ? value.toFixed(1) : String(value ?? '')) as never}
                                    />
                                    {avgFinishData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={entry.color} />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>
                <div className="bg-transparent backdrop-blur-sm border border-white/20 rounded-xl sm:rounded-2xl p-3 sm:p-4">
                    <h4 className="text-[8px] sm:text-[9px] md:text-[10px] font-medium text-white/80 uppercase tracking-wide text-center mb-2 sm:mb-3 md:mb-4">
                        Overtake Efficiency
                    </h4>
                    <div className="h-40 sm:h-48 md:h-60">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={overtakeData} margin={{ top: 5, right: 5, left: 5, bottom: 15 }}>
                                <XAxis 
                                    dataKey="name" 
                                    axisLine={false} 
                                    tickLine={false}
                                    tick={{ fill: '#ffffff80', fontSize: 8 }}
                                />
                                <YAxis hide domain={[-1, 1]} />
                                <Bar dataKey="value" radius={[4, 4, 4, 4]}>
                                    <LabelList 
                                        dataKey="value" 
                                        position="center" 
                                        fill="#ffffff" 
                                        fontSize={14} 
                                        fontWeight="bold"
                                        formatter={((value: number | string | null | undefined) => typeof value === 'number' ? value.toFixed(2) : String(value ?? '')) as never}
                                    />
                                    {overtakeData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={entry.color} />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                    <div className="text-[9px] sm:text-[10px] md:text-xs text-white/60 text-center mt-1 sm:mt-2">
                        <span className="text-green-400">{'\u2265'}0.5 Excellent</span> {'\u2022'} 
                        <span className="text-yellow-400 mx-1">0-0.5 Good</span> {'\u2022'} 
                        <span className="text-red-400">&lt;0 Poor</span>
                    </div>
                </div>
                
                <div className="bg-transparent backdrop-blur-sm border border-white/20 rounded-xl sm:rounded-2xl p-3 sm:p-4">
                    <h4 className="text-[8px] sm:text-[9px] md:text-[10px] font-medium text-white/80 uppercase tracking-wide text-center mb-2 sm:mb-3 md:mb-4">
                        Available Points %
                    </h4>
                    <div className="h-32 sm:h-36 md:h-40 flex items-center justify-center">
                        <div className="relative">
                            <ResponsiveContainer width={110} height={110} className="sm:!w-[130px] sm:!h-[130px] md:!w-[140px] md:!h-[140px]">
                                <PieChart>
                                    <Pie
                                        data={availablePointsData}
                                        cx={55}
                                        cy={55}
                                        innerRadius={28}
                                        outerRadius={48}
                                        dataKey="value"
                                        strokeWidth={0}
                                        startAngle={90}
                                        endAngle={450}
                                    >
                                        {availablePointsData.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill={entry.color} />
                                        ))}
                                    </Pie>
                                </PieChart>
                            </ResponsiveContainer>
                            <div className="absolute inset-0 flex items-center justify-center">
                                <div className="text-center">
                                    <span className="text-white font-bold text-sm sm:text-base md:text-lg">
                                        {fantasy_stats.available_points_percentatge}%
                                    </span>
                                    <div className="text-white/60 text-[9px] sm:text-[10px] md:text-xs">achieved</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="bg-transparent backdrop-blur-sm border border-white/20 rounded-xl sm:rounded-2xl p-3 sm:p-4">
                    <h4 className="text-[8px] sm:text-[9px] md:text-[10px] font-medium text-white/80 uppercase tracking-wide text-center mb-2 sm:mb-3 md:mb-4">
                        Pole to Win Ratio
                    </h4>
                    <div className="h-32 sm:h-36 md:h-40 flex items-center justify-center">
                        <div className="relative">
                            <ResponsiveContainer width={110} height={110} className="sm:!w-[130px] sm:!h-[130px] md:!w-[140px] md:!h-[140px]">
                                <PieChart>
                                    <Pie
                                        data={poleWinData}
                                        cx={55}
                                        cy={55}
                                        innerRadius={28}
                                        outerRadius={48}
                                        dataKey="value"
                                        strokeWidth={0}
                                        startAngle={90}
                                        endAngle={450}
                                    >
                                        {poleWinData.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill={entry.color} />
                                        ))}
                                    </Pie>
                                </PieChart>
                            </ResponsiveContainer>
                            <div className="absolute inset-0 flex items-center justify-center">
                                <div className="text-center">
                                    <span className="text-white font-bold text-sm sm:text-base md:text-lg">
                                        {fantasy_stats.pole_win_conversion}%
                                    </span>
                                    <div className="text-white/60 text-[9px] sm:text-[10px] md:text-xs">success</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
});

DriverStatsCharts.displayName = 'DriverStatsCharts';
