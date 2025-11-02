import { QuickSellContent } from "./QuickSellContent"
import { BuyDriverContent } from "./BuyDriverContent"
import { ListForSaleContent } from "./ListForSaleContent"
import type { ModalMode } from "../modalConfig"

interface TransactionDetailsProps {
    mode: ModalMode,
}

export const TransactionDetails = ({ mode }: TransactionDetailsProps) => {
    if (mode === 'quickSell') return <QuickSellContent/>
    if (mode === 'buyDriver') return <BuyDriverContent />
    if (mode === 'listForSale') return <ListForSaleContent/>
}