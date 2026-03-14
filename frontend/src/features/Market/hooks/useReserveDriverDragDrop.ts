import { useState } from 'react';
import { 
    useSensors, 
    useSensor, 
    PointerSensor,
    type DragEndEvent 
} from '@dnd-kit/core';
import { useSwapReserveDriver } from './useSwapReserveDriver';

interface UseReserveDriverDragDropParams {
    leagueId: number;
    userId: number;
    reserveDriverId?: number | null;
}

export const useReserveDriverDragDrop = ({
    leagueId,
    userId,
    reserveDriverId,
}: UseReserveDriverDragDropParams) => {
    const [swappingDriverIds, setSwappingDriverIds] = useState<{ 
        mainDriver: number; 
        reserve: number 
    } | null>(null);
    
    const { mutateAsync: swapReserve, isPending: isSwapping } = useSwapReserveDriver();

    // Drag & Drop sensors
    const sensors = useSensors(
        useSensor(PointerSensor, {
            activationConstraint: {
                distance: 8, // 8px movement required to start drag
            },
        })
    );

    // Handle drag and drop for reserve driver swap
    const handleDragEnd = async (event: DragEndEvent) => {
        const { active, over } = event;
        
        if (!over || active.id === over.id) return;
        
        // Extract driver IDs from the drag event
        const activeId = Number(active.id.toString().replace('driver-', ''));
        const overId = Number(over.id.toString().replace('driver-', ''));
        
        // Only allow swapping with reserve driver
        const isActiveReserve = reserveDriverId === activeId;
        const isOverReserve = reserveDriverId === overId;
        
        if (!isActiveReserve && !isOverReserve) {
            // Neither is reserve, don't allow swap
            return;
        }
        
        // Determine which driver to make reserve and which is currently reserve
        const driverToMakeReserve = isActiveReserve ? overId : activeId;
        const currentReserveId = isActiveReserve ? activeId : overId;
        
        // Set swapping state to show skeletons
        setSwappingDriverIds({
            mainDriver: driverToMakeReserve,
            reserve: currentReserveId
        });
        
        try {
            await swapReserve({
                leagueId,
                driverId: driverToMakeReserve,
            });
        } finally {
            // Clear swapping state after mutation completes
            setSwappingDriverIds(null);
        }
    };

    return {
        sensors,
        swappingDriverIds,
        isSwapping,
        handleDragEnd,
    };
};
