import { useSortable } from "@dnd-kit/sortable";
import { CSS } from '@dnd-kit/utilities';
import { ReserveDriverSlot } from "./ReserveDriverSlot";
import type { DraggableCardProps } from "./DraggableCard";

interface DraggableReserveSlotProps extends DraggableCardProps {
    loading: boolean;
}

export const DraggableReserveSlot = ({ driver, marketContext, loading = false }: DraggableReserveSlotProps) => {
    const reserveDriverId = driver?.id

    const {
        attributes,
        listeners,
        setNodeRef,
        transform,
        transition,
        isDragging,
    } = useSortable({ 
        id: reserveDriverId ? `driver-${reserveDriverId}` : 'reserve-empty',
        transition: null, // Disable automatic transitions
    });

    // Only apply transform to the card being dragged
    const dragStyle = {
        transform: isDragging ? CSS.Transform.toString(transform) : undefined,
        transition: isDragging ? transition : undefined,
    };

    // Check if reserve driver is being swapped
    const isSwapping = marketContext.swappingDriverIds && driver &&
    (marketContext.swappingDriverIds.mainDriver === driver.id || marketContext.swappingDriverIds.reserve === driver.id);

    return (
        <ReserveDriverSlot
            driver={driver || null}
            isEmpty={!driver}
            dragRef={driver ? setNodeRef : undefined}
            dragStyle={driver ? dragStyle : undefined}
            dragAttributes={driver ? attributes : undefined}
            dragListeners={driver ? listeners : undefined}
            isDragging={isDragging}
            isSwapping={isSwapping ?? undefined}
            marketContext={marketContext}
            loading={loading}
        />
    );
};