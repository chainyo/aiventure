// Game constants
import {
    AudioLines,
    Eye,
    MessageSquareText,
    SquareStack,
    type Icon as IconType
} from "lucide-svelte";


export const CREATE_LAB_COST = 100_000;
export const CREATE_MODEL_COST = 10_000;

export interface Location {
    emoji: string;
    title: string;
    description: string;
    bonuses: string[];
}
export const LOCATIONS: Record<string, Location> = {
    us: { emoji: "🌎", title: "US", description: "Silicon Valley Hub", bonuses: ["+5% Valuation", "+5% Income"] },
    eu: { emoji: "🌍", title: "EU", description: "Research Focus", bonuses: ["+15% Research Speed", "-5% Valuation"] },
    apac: { emoji: "🌏", title: "APAC", description: "Asia Pacific", bonuses: ["+5% Research Speed", "+5% Income"] },
};

export interface ModelCategory {
    icon: typeof IconType;
    description: string;
}
export const MODEL_CATEGORIES: Record<number, ModelCategory> = {
    1: { icon: AudioLines, description: "Audio" },
    2: { icon: Eye, description: "Vision" },
    3: { icon: MessageSquareText, description: "Language" },
    4: { icon: SquareStack, description: "Modal" },
};
