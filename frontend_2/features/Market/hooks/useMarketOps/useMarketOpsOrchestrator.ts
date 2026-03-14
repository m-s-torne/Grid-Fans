import { useBuyFromMarket, useBuyFromUser, useListForSale, useSellToMarket, useUnlistFromSale } from './useMarketOps';

export const useMarketOpsOrchestrator = () => {
    const { mutate: buyFromMarket, isPending: isBuyingFromMarket } = useBuyFromMarket();
    const { mutate: buyFromUser } = useBuyFromUser();
    const { mutate: sellToMarket, isPending: isSellingToMarket } = useSellToMarket();
    const { mutate: listForSale, isPending: isListing } = useListForSale();
    const { mutate: unlistFromSale } = useUnlistFromSale();
    
    return {
        buyFromMarket,
        isBuyingFromMarket,
        buyFromUser,
        sellToMarket,
        isSellingToMarket,
        listForSale,
        isListing,
        unlistFromSale,
    }
}
