import type { DriverWithOwnership } from "@/features/Market/types/marketTypes";
import { useSortable } from "@dnd-kit/sortable";
import { CSS } from '@dnd-kit/utilities';
import { DriverSkeleton } from "./DriverSkeleton";
import { useMarketContext } from "@/core/contexts/MarketContext";
import { MarketDriverCard } from "./MarketDriverCard";

interface DraggableCardProps {
    driver: DriverWithOwnership;
}

export const DraggableCard = ({ driver }: DraggableCardProps) => {
    const {
        swappingDriverIds,
        internalUserId,
        userBudget,
        userDriverCount,
        userTeam,
        handleBuyFromMarket,
        handleBuyFromUser,
        handleSell,
        handleList,
        handleUnlist,
        handleBuyout,
        setExpandedDriver,
    } = useMarketContext()

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
    const isSwapping = swappingDriverIds && 
    (swappingDriverIds.mainDriver === driver.id || swappingDriverIds.reserve === driver.id);

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
        />
        </div>
    </div>
    );
};