import { DndContext, closestCenter } from '@dnd-kit/core';
import { SortableContext } from '@dnd-kit/sortable';
import { MarketDriverList } from './MarketDriverList';
import { useMarketContext } from '@/core/contexts/MarketContext';

const titleMap = {
    'free': 'Free Agent Drivers',
    'for-sale': 'Drivers For Sale',
    'my-drivers': 'My Drivers',
}

const MarketDriverSection = () => {
    const marketContext = useMarketContext()

    // Compute title based on active tab
    const title = titleMap[marketContext.activeTab?? 'free'];

    return (
        <div className="bg-gradient-to-br from-gray-800/40 to-gray-900/40 border border-gray-700/50 backdrop-blur-sm rounded-xl sm:rounded-2xl p-4 sm:p-6">
            {/* Header */}
            <div className="flex items-center justify-between mb-4 sm:mb-6">
                <h2 className="text-lg sm:text-xl lg:text-2xl font-bold text-white">
                    {title}
                </h2>
                <p className="text-gray-400 text-xs sm:text-sm lg:text-base">
                    {marketContext.filteredDrivers.length} {marketContext.filteredDrivers.length === 1 ? 'driver' : 'drivers'}
                </p>
            </div>

            {/* Driver List - with or without DnD */}
            {marketContext.activeTab === 'my-drivers' ? (
                <DndContext
                    sensors={marketContext.sensors}
                    collisionDetection={closestCenter}
                    onDragEnd={marketContext.handleDragEnd}
                >
                    <SortableContext
                        items={marketContext.filteredDrivers.map(d => `driver-${d.id}`)}
                    >
                        <MarketDriverList
                            enableDragDrop={true}
                            marketContext={marketContext}
                        />
                    </SortableContext>
                </DndContext>
            ) : (
                <MarketDriverList 
                    marketContext={marketContext}
                />
            )}
        </div>
    );
};

export default MarketDriverSection;
