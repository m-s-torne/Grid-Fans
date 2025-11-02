import { useMarketContext } from "@/core/contexts/MarketContext";
import { useSortable } from "@dnd-kit/sortable";
import { CSS } from '@dnd-kit/utilities';
import type { DriverWithOwnership } from "../../types/marketTypes";
import { ReserveDriverSlot } from "./ReserveDriverSlot";

interface DraggableDriverSlotProps {
    driver: DriverWithOwnership | undefined;
}

export const DraggableReserveSlot = ({ driver }: DraggableDriverSlotProps) => {
    const {
        swappingDriverIds,
        internalUserId,
        userBudget,
        userDriverCount,
        handleBuyFromMarket,
        handleBuyFromUser,
        handleSell,
        handleList,
        handleUnlist,
        handleBuyout,
        setExpandedDriver,
    } = useMarketContext()

    
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
            currentUserId={internalUserId}
            userBudget={userBudget}
            userDriverCount={userDriverCount}
            reserveDriverId={reserveDriverId}
            onBuyFromMarket={handleBuyFromMarket}
            onBuyFromUser={handleBuyFromUser}
            onSell={handleSell}
            onList={handleList}
            onUnlist={handleUnlist}
            onBuyout={handleBuyout}
            onViewDetails={setExpandedDriver}
            dragRef={driver ? setNodeRef : undefined}
            dragStyle={driver ? dragStyle : undefined}
            dragAttributes={driver ? attributes : undefined}
            dragListeners={driver ? listeners : undefined}
            isDragging={isDragging}
            isSwapping={isSwapping ?? undefined}
        />
    );
};