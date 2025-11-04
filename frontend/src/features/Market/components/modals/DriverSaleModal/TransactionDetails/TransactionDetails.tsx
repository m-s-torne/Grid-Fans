import { QuickSellContent, type QuickSellContentProps } from "./QuickSellContent"
import { BuyDriverContent, type BuyDriverContentProps } from "./BuyDriverContent"
import { ListForSaleContent, type ListForSaleContentProps } from "./ListForSaleContent"
import type { ModalMode } from "@/features/Market/components/modals/DriverSaleModal/modalConfig"
import type { DriverWithOwnership } from "@/features/Market/types/marketTypes";
import type { ComponentType } from "react";

export interface TransactionDetailsProps extends ListForSaleContentProps, BuyDriverContentProps, QuickSellContentProps {
    mode: ModalMode;
    driver: DriverWithOwnership;
}

const CONTENT_COMPONENTS: Record<ModalMode, ComponentType<TransactionDetailsProps>> = {
    quickSell: QuickSellContent,
    buyDriver: BuyDriverContent,
    listForSale: ListForSaleContent,
} as const;

export const TransactionDetails = (props: TransactionDetailsProps) => {
    const { mode } = props;
    const ContentComponent = CONTENT_COMPONENTS[mode];
    return <ContentComponent {...props} />;
}
