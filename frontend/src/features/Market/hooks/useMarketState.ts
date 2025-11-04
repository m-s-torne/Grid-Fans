import { useState } from "react";
import type { DriverWithOwnership } from "@/features/Market/types/marketTypes";

export type Dialog = {
    isOpen: boolean;
    type: 'confirm' | 'success' | 'error' | 'info';
    title: string;
    message: string;
    onConfirm?: () => void;
    confirmText?: string;
}

export type ActiveTab = 'free' | 'for-sale' | 'my-drivers'

export const useMarketStates = () => {
  const [expandedDriver, setExpandedDriver] = useState<DriverWithOwnership | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [activeTab, setActiveTab] = useState<ActiveTab>('free');
  const [buyModalDriver, setBuyModalDriver] = useState<DriverWithOwnership | null>(null);
  const [sellModalDriver, setSellModalDriver] = useState<DriverWithOwnership | null>(null);
  const [listModalDriver, setListModalDriver] = useState<DriverWithOwnership | null>(null);

  // Dialog states
  const [dialog, setDialog] = useState<Dialog>({
      isOpen: false,
      type: 'info',
      title: '',
      message: '',
  });

  return {
    expandedDriver, setExpandedDriver,
    searchQuery, setSearchQuery,
    activeTab, setActiveTab,
    buyModalDriver, setBuyModalDriver,
    sellModalDriver, setSellModalDriver,
    listModalDriver, setListModalDriver,
    dialog, setDialog
  }
}