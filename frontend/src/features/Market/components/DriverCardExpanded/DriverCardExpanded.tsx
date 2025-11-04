import type { DriverWithOwnership } from '@/features/Market/types/marketTypes'
import { GlassCard } from '@/core/components'
import { DriverInfo } from '@/core/components'
import { DriverImage } from '@/core/components'
import { DriverStatsCharts } from './DriverStatsCharts'
import { formatCurrencyPrecise } from '@/features/Market/utils'
import { motion } from 'framer-motion'

interface DriverCardProps {
    d:DriverWithOwnership;
    setExpanded: (name: string | null) => void;
}

export const DriverCardExpanded = ({ d, setExpanded }: DriverCardProps) =>  {
    
    return (
        <div>
            <motion.div
                className="fixed inset-0 backdrop-blur-md bg-black/50 z-[60]"
                onClick={() => setExpanded(null)}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
            />
            {/* Driver number - fixed background outside scrollable container */}
            <motion.div 
                className="fixed sm:top-[5%] top-[20%] sm:left-0 right-0 z-[71] pointer-events-none flex justify-center"
                initial={{
                    opacity: 0,
                }}
                animate={{
                    opacity: 1,
                }}
                exit={{
                    opacity: 0,
                }}
                transition={{ type: "spring", stiffness: 150, damping: 30 }}
            >
                <span
                    className={`
                        block text-[40vw] sm:text-[35vw] md:text-[30vw]
                        select-none
                    `}
                    style={{
                        WebkitTextStroke: "2px rgba(255,255,255,0.10)",
                        color: "transparent",
                    }}
                >
                    {d.driver_number}
                </span>
            </motion.div>
            <GlassCard
                color={d.driver_color}
                motionKey={d.driver_number}
                className="flex flex-col gap-0 rounded-2xl sm:rounded-4xl border-2 sm:border-4 p-0 overflow-y-auto scrollbar-hide"
                initial={{
                    opacity: 0,
                    scale: 0.7,
                    borderRadius: "1rem",
                    boxShadow: "0 0 0px #0000",
                    position: "fixed",
                    top: "50%",
                    left: "50%",
                    width: "60vw",
                    height: "60vh",
                    zIndex: 70,
                    translateX: "-50%",
                    translateY: "-50%",
                }}
                animate={{
                    opacity: 1,
                    scale: 1,
                    borderRadius: "1rem",
                    boxShadow: "0 0 40px #0008",
                    position: "fixed",
                    top: "50%",
                    left: "50%",
                    width: "95vw",
                    height: "95vh",
                    maxHeight: "95vh",
                    zIndex: 70,
                    translateX: "-50%",
                    translateY: "-50%",
                }}
                exit={{
                    opacity: 0,
                    scale: 0.7,
                    boxShadow: "0 0 0px #0000",
                    position: "fixed",
                    width: "60vw",
                    height: "60vh",
                }}
                transition={{ type: "spring", stiffness: 150, damping: 30 }}
            >
            
            {/* Header section - enhanced glass effect with gradient background */}
            <div className="sticky w-full top-0 z-10 px-2 pt-2 pb-3">
                {/* Main header card with enhanced styling */}
                <div className="relative bg-gradient-to-br from-white/25 via-white/15 to-white/5 backdrop-blur-xl border-2 border-white/30 rounded-3xl sm:rounded-[2rem] shadow-2xl overflow-hidden">
                    {/* Subtle inner glow */}
                    <div className="absolute inset-0 bg-gradient-to-br from-white/10 via-transparent to-black/10 rounded-3xl sm:rounded-[2rem]"></div>
                    
                    {/* Content wrapper with relative positioning */}
                    <div className="relative z-10">
                        {/* Price badge */}
                        <div className="absolute top-3 sm:top-4 md:top-5 right-3 sm:right-4 md:right-5 bg-gradient-to-r from-emerald-500 to-green-600 text-white px-4 py-2 sm:px-5 sm:py-2.5 md:px-6 md:py-3 rounded-2xl text-sm sm:text-base md:text-xl font-bold border-2 border-emerald-400/60 shadow-2xl z-20 backdrop-blur-sm">
                            {formatCurrencyPrecise(d.fantasy_stats?.price || 0)}
                        </div>
                        
                        {/* Image and info container */}
                        <div className="relative pt-8 sm:pt-12 md:pt-8 px-4 sm:px-5 md:px-6 pb-4">
                            {/* Driver image - always absolute */}
                            <div className="absolute left-4 sm:left-5 md:left-6 sm:top-3 top-4">
                                <DriverImage
                                    key={d.id}
                                    url={d.headshot_url}
                                    name={d.full_name}
                                    color={d.driver_color}
                                    expanded={true}
                                />
                            </div>
                            
                            {/* Driver info - with left padding to avoid overlap */}
                            <div className="pl-28 sm:pl-32 md:pl-46 pt-2">
                                <DriverInfo
                                    key={d.id}
                                    name={d.full_name}
                                    country={d.country_code || ''}
                                    team={d.team_name || ''}
                                    points={d.season_results?.points || 0}
                                    expanded={true}
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div className="w-full px-2 pb-2">
                {d.season_results && d.fantasy_stats && (
                    <DriverStatsCharts
                        key={d.id}
                        season_results={d.season_results}
                        fantasy_stats={d.fantasy_stats}
                    />
                )}
            </div>
            
            {/* Close button - sticky to stay visible during scroll */}
            <div className="sticky bottom-2 sm:bottom-4 flex justify-end mt-auto pointer-events-none">
                <div 
                    onClick={() => setExpanded(d.full_name)}
                    className="p-2 sm:p-2.5 rounded-lg bg-gray-700/90 hover:bg-gray-600/95 transition-all duration-150 cursor-pointer group backdrop-blur-sm border border-gray-600 shadow-lg pointer-events-auto"
                >
                    <svg 
                        className="w-6 h-6 sm:w-7 sm:h-7 text-gray-200 group-hover:text-white transition-colors" 
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
                </div>
            </div>
        </GlassCard>
        </div>
    )
}
