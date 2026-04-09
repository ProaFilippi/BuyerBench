import type { AppProps } from 'next/app';
import '@/styles/globals.css';
import '@/styles/print.css';

export default function App({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />;
}
