import Link from 'next/link';
import styles from './Layout.module.css';

interface LayoutProps {
  children: React.ReactNode;
  generatedAt?: string;
}

export default function Layout({ children, generatedAt }: LayoutProps) {
  return (
    <div className={styles.root}>
      <header className={styles.header}>
        <div className={styles.headerInner}>
          <Link href="/" className={styles.logo}>
            <span className={styles.logoGlyph}>█</span>
            BUYERBENCH
          </Link>
          <nav className={styles.nav}>
            <Link href="/" className={styles.navLink}>RANKINGS</Link>
            <Link href="/about" className={styles.navLink}>ABOUT</Link>
          </nav>
        </div>
      </header>

      <main className={styles.main}>{children}</main>

      <footer className={styles.footer}>
        <span>BUYERBENCH — AI BUYER AGENT BENCHMARK</span>
        {generatedAt && generatedAt !== 'SAMPLE DATA' && (
          <span>REPORT GENERATED: {generatedAt}</span>
        )}
        {generatedAt === 'SAMPLE DATA' && (
          <span className="tag">SAMPLE DATA — run buyerbench to get live results</span>
        )}
      </footer>
    </div>
  );
}
