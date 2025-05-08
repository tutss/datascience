
# Run application

## Launch API

```
uvicorn app:app --reload --port 8000
```

## Launch application

```
npm run dev
```

# Installing


#### Create Next app

```
npx create-next-app@latest mimir-ui
cd mimir-ui
```

#### Install packages

```
npm install axios
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

#### Edit tailwind.config.js

```
module.exports = {
  content: ["./app/**/*.tsx", "./components/**/*.tsx"],
  theme: {
    extend: {},
  },
  plugins: [],
};
```

#### Replace globals.css

```
@tailwind base;
@tailwind components;
@tailwind utilities;
```

#### Create page.tsx in app

#### Proxy requests on next.config.js

```
module.exports = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
    ];
  },
};
```