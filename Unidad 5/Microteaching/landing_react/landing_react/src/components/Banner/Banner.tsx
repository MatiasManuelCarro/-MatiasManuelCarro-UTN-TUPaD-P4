import styles from './Banner.module.css';

const Banner = () => {
  return (
    <section id="banner" className={styles.banner}>
      <div className={styles.inner}>
        <h1 className={styles.title}>
          La plataforma que impulsa tu negocio
        </h1>
        <p className={styles.subtitle}>
          Herramientas modernas para equipos ambiciosos. Lanza más rápido y
          escala sin preocuparte por la infraestructura.
        </p>
        <div className={styles.actions}>
          <a href="#contact" className={styles.btnPrimary}>
            Empezar gratis
          </a>
          <a href="#features" className={styles.btnSecondary}>
            Ver características
          </a>
        </div>
      </div>
    </section>
  );
};

export default Banner;
