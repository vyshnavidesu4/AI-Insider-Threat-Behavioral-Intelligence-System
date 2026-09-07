import type { Config } from 'tailwindcss';

const config: Config = {
  darkMode: ['class'],
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        // SOC Real Tool Palette (Deep Slate base, high contrast borders, zero neon)
        soc: {
          bg: '#090d16',          // Deep console root background
          panel: '#0f172a',       // Slate 900 panel background
          elevated: '#1e293b',    // Slate 800 elevated hover/header background
          card: '#0f172a',        // Container background
          subtle: '#172033',      // Subtle table row alternate
          border: '#334155',      // Slate 700 standard hairline border
          borderMuted: '#1e293b', // Slate 800 secondary border
          borderFocus: '#475569', // Focused control border
        },
        // Monochromatic Foregrounds
        socText: {
          primary: '#f8fafc',     // Slate 50 off-white primary text
          secondary: '#94a3b8',   // Slate 400 secondary metadata
          muted: '#64748b',       // Slate 500 table headers / timestamps
          disabled: '#475569',    // Slate 600 disabled state
        },
        // Muted Status Palette (Strictly non-neon, professional SOC grading)
        threat: {
          // Critical (Score 80-100)
          critical: '#ef4444',
          criticalBg: '#450a0a',
          criticalBorder: '#991b1b',
          criticalText: '#fca5a5',

          // High (Score 60-79)
          high: '#f97316',
          highBg: '#431407',
          highBorder: '#9a3412',
          highText: '#fdba74',

          // Medium / Elevated (Score 40-59)
          medium: '#f59e0b',
          mediumBg: '#451a03',
          mediumBorder: '#b45309',
          mediumText: '#fde68a',

          // Low (Score 20-39)
          low: '#3b82f6',
          lowBg: '#172554',
          lowBorder: '#1e40af',
          lowText: '#93c5fd',

          // Normal / Benign (Score 0-19)
          benign: '#10b981',
          benignBg: '#064e3b',
          benignBorder: '#065f46',
          benignText: '#6ee7b7',

          // Informational / Neutral
          info: '#64748b',
          infoBg: '#0f172a',
          infoBorder: '#334155',
          infoText: '#cbd5e1',
        },
      },
      fontFamily: {
        sans: [
          'Inter',
          '-apple-system',
          'BlinkMacSystemFont',
          'Segoe UI',
          'Roboto',
          'sans-serif',
        ],
        mono: [
          'JetBrains Mono',
          'ui-monospace',
          'SFMono-Regular',
          'Menlo',
          'Monaco',
          'Consolas',
          'monospace',
        ],
      },
      fontSize: {
        '2xs': '0.6875rem', // 11px - ultra-dense SOC tables
        'xs': '0.75rem',    // 12px
        'sm': '0.8125rem',  // 13px - standard data rows
        'base': '0.875rem', // 14px - standard labels
        'lg': '1rem',       // 16px - panel headings
        'xl': '1.125rem',   // 18px
      },
      borderRadius: {
        none: '0px',
        sm: '2px',
        DEFAULT: '3px',
        md: '4px',
        lg: '6px',
      },
      boxShadow: {
        // Flat, crisp hairline inset shadows rather than blurry floats
        'soc-panel': 'inset 0 1px 0 0 rgba(255, 255, 255, 0.05), 0 1px 2px 0 rgba(0, 0, 0, 0.5)',
        'soc-table': '0 1px 3px 0 rgba(0, 0, 0, 0.6)',
      },
    },
  },
  plugins: [],
};

export default config;
