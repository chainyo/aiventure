import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
	return twMerge(clsx(inputs));
}

export function formatNumber(num: number, threshold: number = 1000): string {
	const absNum = Math.abs(num);
	if (absNum < threshold) {
		return (Math.round(num * 100) / 100).toLocaleString(undefined, {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
	}

	if (absNum >= 1e12) return (num / 1e12).toFixed(1) + 'T';
	if (absNum >= 1e9) return (num / 1e9).toFixed(1) + 'B';
	if (absNum >= 1e6) return (num / 1e6).toFixed(1) + 'M';
	if (absNum >= 1e3) return (num / 1e3).toFixed(1) + 'K';
	return num.toString();
}
