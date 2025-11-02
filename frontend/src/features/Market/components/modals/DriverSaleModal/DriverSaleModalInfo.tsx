import type { DriverWithOwnership } from '@/features/Market/types/marketTypes';

interface DriverSaleModalInfoProps {
  driver: DriverWithOwnership | null;
}

export const DriverSaleModalInfo = ({ driver }: DriverSaleModalInfoProps) => {
  return (
    <div className="bg-black/30 rounded-xl p-3 border border-gray-700/50">
      <div className="flex items-center gap-3">
        {driver!.headshot_url && (
          <img
            src={driver!.headshot_url}
            alt={driver!.full_name}
            className="w-14 h-14 rounded-full object-cover object-top border-2"
            style={{ borderColor: driver!.driver_color || '#888' }}
          />
        )}
        <div className="flex-1">
          <h3 className="text-lg font-bold text-white">{driver!.full_name}</h3>
          <p className="text-gray-400 text-xs">{driver!.team_name}</p>
        </div>
      </div>
    </div>
  );
};
