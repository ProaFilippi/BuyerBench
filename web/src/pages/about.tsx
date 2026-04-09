import Layout from '@/components/Layout';
import styles from './about.module.css';

export default function AboutPage() {
  return (
    <Layout>
      <section className={styles.hero}>
        <h1 className={styles.headline}>ABOUT BUYERBENCH</h1>
        <p className={styles.body}>
          BuyerBench is an open-source benchmark framework for evaluating AI buyer agents
          across three pillars: <strong>Agent Intelligence &amp; Operational Capability</strong>,{' '}
          <strong>Economic Decision Quality &amp; Behavioral Robustness</strong>, and{' '}
          <strong>Security, Compliance &amp; Market Readiness</strong>.
        </p>
      </section>
    </Layout>
  );
}
