/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: [{
      light: {

        "primary": "#38bdf8",

        "secondary": "#001ac6",

        "accent": "#bcd0ff",

        "neutral": "#362b3b",

        "base-100": "#f3f4f6",

        "info": "#55a5e7",

        "success": "#4eda96",

        "warning": "#a17c02",

        "error": "#ea577e",
      },
    },
    {
      dark: {

        "primary": "#d4bcf4",

        "secondary": "#0891b2",

        "accent": "#382d93",

        "neutral": "#1b1d27",

        "base-100": "#374151",

        "info": "#358ce3",

        "success": "#28d283",

        "warning": "#efb46b",

        "error": "#ee638f",
      },
    },
    ],
  },
}

