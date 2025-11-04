/**
 * Market and ownership related types
 */

// ============================================================================
// DRIVER TYPES
// ============================================================================

/**
 * Base Driver type - used across the application
 * Contains core driver info and stats without ownership data
 */
export interface Driver {
  id: number;
  driver_number: number;
  full_name: string;
  acronym: string;
  driver_color: string;
  country_code: string | null;
  headshot_url: string;
  team_name?: string;
  
  // Stats - estructura real del backend
  season_results?: {
    points: number;
    poles: number;
    podiums: number;
    fastest_laps: number;
    victories: number;
    sprint_podiums: number;
    sprint_victories: number;
    sprint_poles: number;
  };
  fantasy_stats?: {
    price: number;
    avg_finish: number;
    avg_grid_position: number;
    pole_win_conversion: number;
    overtake_efficiency: number;
    available_points_percentatge: number;
  };
}

// ============================================================================
// OWNERSHIP TYPES
// ============================================================================

export interface DriverOwnership {
  driver_id: number;
  league_id: number;
  owner_id: number | null; // null = free agent
  is_listed_for_sale: boolean;
  acquisition_price: number; // Price originally paid by current owner
  asking_price: number | null; // Price when listed for sale (null when not listed)
  locked_until: string | null; // ISO datetime string
  created_at: string;
  updated_at: string;
}

type Transaction = 'buy_from_market' | 'buy_from_user' | 'sell_to_market' | 'buyout_clause' | 'emergency_assignment';
export interface MarketTransaction {
  id: number;
  driver_id: number;
  league_id: number;
  seller_id: number | null; // null for free agent purchases
  buyer_id: number;
  transaction_price: number;
  transaction_type: Transaction;
  transaction_date: string;
}

export interface BuyoutClauseHistory {
  id: number;
  league_id: number;
  buyer_id: number;
  victim_id: number;
  driver_id: number;
  buyout_price: number;
  buyout_date: string;
  season_year: number;
}

// Request types
export interface BuyDriverFromMarketRequest {
  buyer_user_id: number;
}

export interface BuyDriverFromUserRequest {
  buyer_user_id: number;
  seller_user_id: number;
}

export interface SellDriverToMarketRequest {
  seller_user_id: number;
}

export interface ListDriverForSaleRequest {
  owner_user_id: number;
  asking_price?: number;
}

export interface UnlistDriverRequest {
  owner_user_id: number;
}

export interface BuyoutClauseRequest {
  buyer_user_id: number;
  victim_user_id: number;
}

// Response types
export interface BuyDriverResponse {
  success: boolean;
  driver_id: number;
  price: number;
  locked_until: string;
  new_budget: number;
}

export interface BuyFromUserResponse {
  success: boolean;
  driver_id: number;
  price: number;
  seller_id: number;
  locked_until: string;
  buyer_new_budget: number;
  seller_new_budget: number;
}

export interface SellDriverResponse {
  success: boolean;
  driver_id: number;
  refund: number;
  new_budget: number;
}

export interface ListDriverResponse {
  success: boolean;
  driver_id: number;
  asking_price: number;
  is_listed: boolean;
}

type Replacement = 'reserve_promoted' | 'emergency_tier_c' | 'reserve_removed';
export interface BuyoutClauseResponse {
  success: boolean;
  driver_id: number;
  buyout_price: number;
  buyer_new_budget: number;
  victim_new_budget: number;
  locked_until: string;
  replacement_info: {
    auto_replaced: boolean;
    replacement_type: Replacement;
    emergency_driver_id?: number;
    message: string;
  } | null;
}

// ============================================================================
// EXTENDED DRIVER TYPES
// ============================================================================

/**
 * Driver with ownership information - extends base Driver
 * Used in Market context where ownership matters
 */
export interface DriverWithOwnership extends Driver {
  // base_price removed - not used, fantasy_stats.price is the dynamic market price
  
  // Ownership info
  ownership: DriverOwnership | null;
  
  // Derived properties for UI convenience
  isOwned: boolean;
  isOwnedByMe: boolean;
  isFreeAgent: boolean;
  isForSale: boolean;
  isLocked: boolean;
  canBuyout: boolean;
  ownerName?: string;
}

// ============================================================================
// MARKET FILTERS
// ============================================================================
export type MarketFilter = 'all' | 'free' | 'owned' | 'for-sale' | 'locked';

export interface MarketFilters {
  filter: MarketFilter;
  searchQuery: string;
  sortBy: 'name' | 'price' | 'points';
  sortOrder: 'asc' | 'desc';
}

// ============================================================================
// MARKET COMPONENT PROPS
// ============================================================================

/**
 * Base props shared by market components
 * Contains user context and action callbacks
 * Extracted to avoid duplication between MarketDriverCard and MarketDriverList
 */
export interface MarketComponentBaseProps {
  currentUserId: number;
  userBudget: number;
  userDriverCount: number;
  reserveDriverId?: number | null;
  onBuyFromMarket?: (driverId: number) => void;
  onBuyFromUser?: (driverId: number) => void;
  onSell?: (driverId: number) => void;
  onList?: (driverId: number) => void;
  onUnlist?: (driverId: number) => void;
  onBuyout?: (driverId: number) => void;
  onViewDetails?: (driver: DriverWithOwnership) => void;
}

/**
 * Props for MarketDriverCard component
 * Extends base props with driver-specific fields
 */

/**
 * Props for MarketDriverList component
 * Extends base props with list-specific fields
 */
