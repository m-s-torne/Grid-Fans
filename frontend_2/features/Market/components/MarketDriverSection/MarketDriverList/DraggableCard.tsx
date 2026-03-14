'use client';

import type { DriverWithOwnership } from "@/features/Market/types/marketTypes";
import { useSortable } from "@dnd-kit/sortable";
import { CSS } from '@dnd-kit/utilities';
import { DriverSkeleton } from "./DriverSkeleton";
import { MarketDriverCard, type MarketDriverCardProps } from "./MarketDriverCard";
import type { UseMarketHandlersReturn } from "@/features/Market/hooks/useMarketHandlers/useMarketHandlers";
import type { SwappingIds } from "@/lib/contexts/MarketContext";

export interface DraggableCardProps extends MarketDriverCardProps {
    driver: DriverWithOwnership;
    handlers: UseMarketHandlersReturn;
    reserveDriverId: number | null;
    swappingDriverIds: SwappingIds | null;
}

export const DraggableCard = ({ 
    driver,
    handlers,
    reserveDriverId,
    swappingDriverIds,
    userState,
    setExpandedDriver,
}: DraggableCardProps) => {
    
    const {
        attributes,
        listeners,
        setNodeRef,
        transform,
        transition,
        isDragging,
    } = useSortable({ 
        id: `driver-${driver.id}`,
        transition: null,
    });

    const isSwapping = swappingDriverIds && 
        (swappingDriverIds.mainDriver === driver.id || swappingDriverIds.reserve === driver.id);

    const style = {
        transform: isDragging ? CSS.Transform.toString(transform) : undefined,
        transition: isDragging ? transition : undefined,
        opacity: isDragging ? 0.5 : 1,
    };

    if (isSwapping) {
        return <DriverSkeleton />;
    }

    return (
    <div>
        <div
            ref={setNodeRef}
            style={style}
            {...attributes}
            {...listeners}
            className="touch-none cursor-grab active:cursor-grabbing"
        >
            <MarketDriverCard
                driver={driver}
                reserveDriverId={reserveDriverId}
                userState={userState}
                handlers={handlers}
                setExpandedDriver={setExpandedDriver}
            />
        </div>
    </div>
    );
};
