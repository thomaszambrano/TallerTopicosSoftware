/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        canvas: "var(--surface)",
        ink: "var(--ink)",
        muted: "var(--muted)",
        line: "var(--line)",
        accent: {
          DEFAULT: "var(--accent)",
          ink: "var(--accent-ink)",
          soft: "var(--accent-soft)",
        },
        surface: {
          raised: "var(--surface-raised)",
          sunken: "var(--surface-sunken)",
        },
      },
      fontFamily: {
        display: [
          "Familjen Grotesk",
          "ui-sans-serif",
          "system-ui",
          "sans-serif",
        ],
        sans: [
          "Public Sans",
          "ui-sans-serif",
          "system-ui",
          "-apple-system",
          "Segoe UI",
          "sans-serif",
        ],
        mono: [
          "JetBrains Mono",
          "ui-monospace",
          "SFMono-Regular",
          "Menlo",
          "monospace",
        ],
      },
      fontSize: {
        "display-xl": ["clamp(2.5rem, 4vw + 1rem, 4.75rem)", { lineHeight: "0.96", letterSpacing: "-0.02em" }],
        "display-lg": ["clamp(2rem, 3vw + 0.75rem, 3.25rem)", { lineHeight: "1", letterSpacing: "-0.02em" }],
        "display-md": ["clamp(1.5rem, 1.5vw + 1rem, 2.25rem)", { lineHeight: "1.05", letterSpacing: "-0.015em" }],
      },
      letterSpacing: {
        tightish: "-0.011em",
        eyebrow: "0.18em",
      },
      boxShadow: {
        edge: "0 1px 0 0 var(--line)",
        focus: "0 0 0 3px color-mix(in oklch, var(--accent) 22%, transparent)",
      },
      borderRadius: {
        sm: "4px",
        DEFAULT: "8px",
        lg: "14px",
        xl: "20px",
      },
      spacing: {
        gutter: "clamp(1rem, 2vw, 2rem)",
        section: "clamp(2.5rem, 5vw, 4.5rem)",
      },
      maxWidth: {
        prose: "65ch",
        page: "1200px",
      },
    },
  },
  plugins: [],
};
