import type { DriverWithOwnership } from "@/features/Market/types/marketTypes";
import { useSortable } from "@dnd-kit/sortable";
import { CSS } from '@dnd-kit/utilities';
import { DriverSkeleton } from "./DriverSkeleton";
import { MarketDriverCard } from "./MarketDriverCard";
import type { MarketContext } from "@/core/contexts/MarketContext";

export interface DraggableCardProps {
    driver: DriverWithOwnership;
    marketContext: MarketContext;
}

export const DraggableCard = ({ 
    driver,
    marketContext,
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
        transition: null, // Disable automatic transitions
    });

    // Check if this driver is being swapped
    const isSwapping = marketContext.swappingDriverIds && 
        (marketContext.swappingDriverIds.mainDriver === driver.id || marketContext.swappingDriverIds.reserve === driver.id);

    // Only apply transform to the card being dragged, not to other cards
    const style = {
        transform: isDragging ? CSS.Transform.toString(transform) : undefined,
        transition: isDragging ? transition : undefined,
        opacity: isDragging ? 0.5 : 1,
    };

    // Show skeleton if swapping
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
                internalUserId={marketContext.internalUserId}
                reserveDriverId={marketContext.userTeam!.reserve_driver_id}
                userBudget={marketContext.userBudget}
                userDriverCount={marketContext.userDriverCount}
                handleBuyFromMarket={marketContext.handleBuyFromMarket}
                handleBuyFromUser={marketContext.handleBuyFromUser}
                handleSell={marketContext.handleSell}
                handleList={marketContext.handleList}
                handleUnlist={marketContext.handleUnlist}
                handleBuyout={marketContext.handleBuyout}
                setExpandedDriver={marketContext.setExpandedDriver}
            />
        </div>
    </div>
    );
};