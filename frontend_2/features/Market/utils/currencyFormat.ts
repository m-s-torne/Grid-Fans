/**
 * Currency formatting utilities
 * 
 * Backend stores all monetary values as INTEGER in base units (dollars).
 * Frontend converts to millions for display without losing precision.
 */

export function formatCurrency(
  value: number,
  options: {
    decimals?: number;
    prefix?: boolean;
    suffix?: boolean;
    removeTrailingZeros?: boolean;
  } = {}
): string {
  const {
    decimals,
    prefix = true,
    suffix = true,
    removeTrailingZeros = false,
  } = options;

  const millions = value / 1_000_000;

  let formatted: string;
  if (decimals !== undefined) {
    formatted = millions.toFixed(decimals);
  } else {
    formatted = millions.toString();
  }

  if (removeTrailingZeros && formatted.includes('.')) {
    formatted = formatted.replace(/\.?0+$/, '');
  }

  const prefixStr = prefix ? '$' : '';
  const suffixStr = suffix ? 'M' : '';

  return `${prefixStr}${formatted}${suffixStr}`;
}

export function formatCurrencyCompact(value: number): string {
  return formatCurrency(value, { decimals: 1 });
}

export function formatCurrencyPrecise(value: number): string {
  return formatCurrency(value, { removeTrailingZeros: true });
}

export function formatCurrencyNumber(value: number, decimals?: number): string {
  return formatCurrency(value, { decimals, prefix: false, suffix: false });
}

export function parseCurrencyInput(input: string): number {
  const cleaned = input.replace(/[^0-9.-]/g, '');
  const value = parseFloat(cleaned);
  
  if (isNaN(value)) {
    return 0;
  }

  if (input.toUpperCase().includes('M')) {
    return Math.floor(value * 1_000_000);
  }
  
  return Math.floor(value);
}
