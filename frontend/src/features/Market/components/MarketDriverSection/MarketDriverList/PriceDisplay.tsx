import { formatCurrency } from '@/features/Market/utils';

interface PriceDisplayProps {
  price: number;
  type?: 'base' | 'buyout' | 'sale' | 'refund';
  showIcon?: boolean;
  compact?: boolean;
}

export const PriceDisplay = ({ 
  price, 
  type = 'base', 
  showIcon = true,
  compact = false 
}: PriceDisplayProps) => {
  const priceInMillions = formatCurrency(price, { prefix: false, suffix: false, removeTrailingZeros: true });

  const getStyles = () => {
    switch (type) {
      case 'buyout':
        return {
          bg: 'bg-orange-600/80',
          border: 'border-orange-400/60',
          text: 'text-orange-50',
          badge: '130%',
          badgeBg: 'bg-orange-700',
          icon: '🔥',
        };
      case 'sale':
        return {
          bg: 'bg-yellow-500/70',
          border: 'border-yellow-200/50',
          text: 'text-yellow-50',
          badge: null,
          badgeBg: '',
          icon: '💰',
        };
      case 'refund':
        return {
          bg: 'bg-red-500/70',
          border: 'border-red-200/50',
          text: 'text-red-50',
          badge: '80%',
          badgeBg: 'bg-red-700',
          icon: '💸',
        };
      default:
        return {
          bg: 'bg-green-500/70',
          border: 'border-green-200/50',
          text: 'text-purple-50',
          badge: null,
          badgeBg: '',
          icon: '💵',
        };
    }
  };

  const styles = getStyles();

  if (compact) {
    return (
      <div className={`inline-flex items-center gap-1 px-2 py-1 rounded ${styles.bg} border ${styles.border}`}>
        {showIcon && <span className="text-xs">{styles.icon}</span>}
        <span className={`${styles.text} font-bold text-xs`}>
          ${priceInMillions}M
        </span>
        {styles.badge && (
          <span className={`text-[9px] px-1 rounded ${styles.badgeBg} ${styles.text} font-bold`}>
            {styles.badge}
          </span>
        )}
      </div>
    );
  }

  return (
    <div className={`text-center p-2 ${styles.bg} rounded border ${styles.border} relative`}>
      <div className="flex items-center justify-center gap-1">
        {showIcon && <span className="text-sm">{styles.icon}</span>}
        <p className="text-purple-200 text-xs">
          {type === 'buyout' && 'Buyout'}
          {type === 'sale' && 'Sale Price'}
          {type === 'refund' && 'Refund'}
          {type === 'base' && 'Market Price'}
        </p>
      </div>
      <p className={`${styles.text} font-bold text-sm`}>
        ${priceInMillions}M
      </p>
      {styles.badge && (
        <div className={`absolute -top-1 -right-1 text-[9px] px-1.5 py-0.5 rounded-full ${styles.badgeBg} ${styles.text} font-bold border ${styles.border}`}>
          {styles.badge}
        </div>
      )}
    </div>
  );
};
