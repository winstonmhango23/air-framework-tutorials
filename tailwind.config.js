/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.{html,js}", "./static/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        background: 'var(--background)',
        foreground: 'var(--foreground)',
        card: 'var(--card)',
        'card-foreground': 'var(--card-foreground)',
        popover: 'var(--popover)',
        'popover-foreground': 'var(--popover-foreground)',
        primary: 'var(--primary)',
        'primary-foreground': 'var(--primary-foreground)',
        secondary: 'var(--secondary)',
        'secondary-foreground': 'var(--secondary-foreground)',
        muted: 'var(--muted)',
        'muted-foreground': 'var(--muted-foreground)',
        accent: 'var(--accent)',
        'accent-foreground': 'var(--accent-foreground)',
        destructive: 'var(--destructive)',
        'destructive-foreground': 'var(--destructive-foreground)',
        border: 'var(--border)',
        input: 'var(--input)',
        ring: 'var(--ring)',
        'chart-1': 'var(--chart-1)',
        'chart-2': 'var(--chart-2)',
        'chart-3': 'var(--chart-3)',
        'chart-4': 'var(--chart-4)',
        'chart-5': 'var(--chart-5)',
        sidebar: 'var(--sidebar)',
        'sidebar-foreground': 'var(--sidebar-foreground)',
        'sidebar-primary': 'var(--sidebar-primary)',
        'sidebar-primary-foreground': 'var(--sidebar-primary-foreground)',
        'sidebar-accent': 'var(--sidebar-accent)',
        'sidebar-accent-foreground': 'var(--sidebar-accent-foreground)',
        'sidebar-border': 'var(--sidebar-border)',
        'sidebar-ring': 'var(--sidebar-ring)',
      },
      borderRadius: {
        DEFAULT: 'var(--radius)',
      }
    },
  },
  plugins: [
    function({ addUtilities }) {
      const newUtilities = {
        '.bg-background': {
          'background-color': 'var(--background)',
        },
        '.text-foreground': {
          'color': 'var(--foreground)',
        },
        '.bg-card': {
          'background-color': 'var(--card)',
        },
        '.text-card-foreground': {
          'color': 'var(--card-foreground)',
        },
        '.bg-popover': {
          'background-color': 'var(--popover)',
        },
        '.text-popover-foreground': {
          'color': 'var(--popover-foreground)',
        },
        '.bg-primary': {
          'background-color': 'var(--primary)',
        },
        '.text-primary-foreground': {
          'color': 'var(--primary-foreground)',
        },
        '.bg-secondary': {
          'background-color': 'var(--secondary)',
        },
        '.text-secondary-foreground': {
          'color': 'var(--secondary-foreground)',
        },
        '.bg-muted': {
          'background-color': 'var(--muted)',
        },
        '.text-muted-foreground': {
          'color': 'var(--muted-foreground)',
        },
        '.bg-accent': {
          'background-color': 'var(--accent)',
        },
        '.text-accent-foreground': {
          'color': 'var(--accent-foreground)',
        },
        '.bg-destructive': {
          'background-color': 'var(--destructive)',
        },
        '.text-destructive-foreground': {
          'color': 'var(--destructive-foreground)',
        },
        '.border-border': {
          'border-color': 'var(--border)',
        },
        '.bg-sidebar': {
          'background-color': 'var(--sidebar)',
        },
        '.text-sidebar-foreground': {
          'color': 'var(--sidebar-foreground)',
        },
        '.bg-sidebar-primary': {
          'background-color': 'var(--sidebar-primary)',
        },
        '.text-sidebar-primary-foreground': {
          'color': 'var(--sidebar-primary-foreground)',
        },
        '.bg-sidebar-accent': {
          'background-color': 'var(--sidebar-accent)',
        },
        '.text-sidebar-accent-foreground': {
          'color': 'var(--sidebar-accent-foreground)',
        },
        '.border-sidebar-border': {
          'border-color': 'var(--sidebar-border)',
        },
        '.text-sidebar-ring': {
          'color': 'var(--sidebar-ring)',
        }
      }
      addUtilities(newUtilities, ['responsive', 'hover'])
    }
  ],
  darkMode: 'class',
}