import { useSortable } from "@dnd-kit/sortable";
import { CSS } from '@dnd-kit/utilities';
import { ReserveDriverSlot } from "./ReserveDriverSlot";
import type { SwappingIds } from "@/core/contexts/MarketContext";
import type { MarketDriverCardProps } from "./MarketDriverCard";

interface DraggableReserveSlotProps extends MarketDriverCardProps {
    loading: boolean;
    swappingDriverIds: SwappingIds | null;
}

export const DraggableReserveSlot = ({ 
    driver, 
    swappingDriverIds,
    userState,
    handlers,
    setExpandedDriver, 
    loading = false
}: DraggableReserveSlotProps) => {
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
    const isSwapping = swappingDriverIds && driver &&
    (swappingDriverIds.mainDriver === driver.id || swappingDriverIds.reserve === driver.id);


    return (
        <ReserveDriverSlot
            driver={driver || null}
            isEmpty={!driver}
            dragRef={driver ? setNodeRef : undefined}
            dragStyle={driver ? dragStyle : undefined}
            dragAttributes={driver ? attributes : undefined}
            dragListeners={driver ? listeners : undefined}
            loading={loading}
            isDragging={isDragging}
            isSwapping={isSwapping ?? undefined}
            reserveDriverId={reserveDriverId ?? null}
            userState={userState}
            handlers={handlers}
            setExpandedDriver={setExpandedDriver}     
        />
    );
};