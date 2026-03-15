'use client';

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

    const sensors = useSensors(
        useSensor(PointerSensor, {
            activationConstraint: {
                distance: 8,
            },
        })
    );

    const handleDragEnd = async (event: DragEndEvent) => {
        const { active, over } = event;
        
        if (!over || active.id === over.id) return;
        
        const activeId = Number(active.id.toString().replace('driver-', ''));
        const overId = Number(over.id.toString().replace('driver-', ''));
        
        const isActiveReserve = reserveDriverId === activeId;
        const isOverReserve = reserveDriverId === overId;
        
        if (!isActiveReserve && !isOverReserve) {
            return;
        }
        
        const driverToMakeReserve = isActiveReserve ? overId : activeId;
        const currentReserveId = isActiveReserve ? activeId : overId;
        
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
