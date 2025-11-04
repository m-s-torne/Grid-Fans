import type { ModalMode } from "./modalConfig";

interface CantProceedBadgeProps {
  mode: ModalMode;
}

export const CantProceedBadge = ({ mode }: CantProceedBadgeProps) => {
  return (
    <div className="bg-red-900/20 border border-red-500/50 rounded-lg p-2">
      <div className="flex items-start gap-1.5">
        <svg className="w-4 h-4 text-red-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <div>
          <p className="text-red-400 font-medium text-[11px]">
            Cannot {mode === 'quickSell' ? 'sell' : 'list'} this driver
          </p>
          <p className="text-red-300/80 text-[10px] mt-0.5">
            You must maintain at least 3 drivers in your team
          </p>
        </div>
      </div>
    </div>
  );
};
