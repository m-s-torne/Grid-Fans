import { http } from '@/lib/axios';
import type {
  DriverOwnership,
  MarketTransaction,
  BuyoutClauseHistory,
  BuyDriverFromMarketRequest,
  BuyDriverResponse,
  BuyDriverFromUserRequest,
  BuyFromUserResponse,
  SellDriverToMarketRequest,
  SellDriverResponse,
  ListDriverForSaleRequest,
  ListDriverResponse,
  UnlistDriverRequest,
  BuyoutClauseRequest,
  BuyoutClauseResponse,
  DriverWithOwnership,
} from '@/lib/types/marketTypes';

class MarketService {
  async getDriverOwnerships(leagueId: number): Promise<DriverOwnership[]> {
    const response = await http.get<DriverOwnership[]>(
      `/leagues/${leagueId}/driver-ownership`
    );
    return response.data;
  }

  async getDriverOwnership(
    leagueId: number,
    driverId: number
  ): Promise<DriverOwnership> {
    const response = await http.get<DriverOwnership>(
      `/leagues/${leagueId}/driver-ownership/${driverId}`
    );
    return response.data;
  }

  async getFreeDrivers(leagueId: number): Promise<DriverWithOwnership[]> {
    const response = await http.get<DriverWithOwnership[]>(
      `/leagues/${leagueId}/market/free-drivers`
    );
    return response.data;
  }

  async getDriversForSale(leagueId: number): Promise<DriverWithOwnership[]> {
    const response = await http.get<DriverWithOwnership[]>(
      `/leagues/${leagueId}/market/for-sale`
    );
    return response.data;
  }

  async getUserDrivers(
    leagueId: number,
    userId: number | string
  ): Promise<DriverWithOwnership[]> {
    const response = await http.get<DriverWithOwnership[]>(
      `/leagues/${leagueId}/market/user-drivers/${userId}`
    );
    return response.data;
  }

  async buyDriverFromMarket(
    leagueId: number,
    driverId: number,
    request: BuyDriverFromMarketRequest
  ): Promise<BuyDriverResponse> {
    const response = await http.post<BuyDriverResponse>(
      `/leagues/${leagueId}/market/buy-from-market/${driverId}`,
      request
    );
    return response.data;
  }

  async buyDriverFromUser(
    leagueId: number,
    driverId: number,
    request: BuyDriverFromUserRequest
  ): Promise<BuyFromUserResponse> {
    const response = await http.post<BuyFromUserResponse>(
      `/leagues/${leagueId}/market/buy-from-user/${driverId}`,
      request
    );
    return response.data;
  }

  async sellDriverToMarket(
    leagueId: number,
    driverId: number,
    request: SellDriverToMarketRequest
  ): Promise<SellDriverResponse> {
    const response = await http.post<SellDriverResponse>(
      `/leagues/${leagueId}/market/sell-to-market/${driverId}`,
      request
    );
    return response.data;
  }

  async listDriverForSale(
    leagueId: number,
    driverId: number,
    request: ListDriverForSaleRequest
  ): Promise<ListDriverResponse> {
    const response = await http.post<ListDriverResponse>(
      `/leagues/${leagueId}/market/list-for-sale/${driverId}`,
      request
    );
    return response.data;
  }

  async unlistDriverFromSale(
    leagueId: number,
    driverId: number,
    request: UnlistDriverRequest
  ): Promise<ListDriverResponse> {
    const response = await http.delete<ListDriverResponse>(
      `/leagues/${leagueId}/market/list-for-sale/${driverId}`,
      { data: request }
    );
    return response.data;
  }

  async executeBuyoutClause(
    leagueId: number,
    driverId: number,
    request: BuyoutClauseRequest
  ): Promise<BuyoutClauseResponse> {
    const response = await http.post<BuyoutClauseResponse>(
      `/leagues/${leagueId}/market/buyout-clause/${driverId}`,
      request
    );
    return response.data;
  }

  async getMarketTransactions(leagueId: number): Promise<MarketTransaction[]> {
    const response = await http.get<MarketTransaction[]>(
      `/leagues/${leagueId}/market/transactions`
    );
    return response.data;
  }

  async getBuyoutHistory(leagueId: number): Promise<BuyoutClauseHistory[]> {
    const response = await http.get<BuyoutClauseHistory[]>(
      `/leagues/${leagueId}/market/buyout-history`
    );
    return response.data;
  }
}

export const marketService = new MarketService();
