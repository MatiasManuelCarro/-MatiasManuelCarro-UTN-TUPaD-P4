import styles from './Footer.module.css';

const columns = [
  {
    title: 'Producto',
    links: ['Características', 'Precios', 'Changelog', 'Roadmap'],
  },
  {
    title: 'Empresa',
    links: ['Sobre nosotros', 'Blog', 'Prensa', 'Careers'],
  },
  {
    title: 'Soporte',
    links: ['Documentación', 'API', 'Comunidad', 'Contacto'],
  },
];

const Footer = () => {
  const year = new Date().getFullYear();

  return (
    <footer className={styles.footer}>
      <div className={styles.top}>
        <div>
          <p className={styles.logo}>Launchly</p>
          <p className={styles.brandDesc}>
            La plataforma para equipos que quieren construir grandes productos.
          </p>
        </div>

        {columns.map((col) => (
          <div key={col.title}>
            <p className={styles.colTitle}>{col.title}</p>
            <ul className={styles.colLinks}>
              {col.links.map((link) => (
                <li key={link}>
                  <a href="#">{link}</a>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>

      <div className={styles.bottom}>
        <p className={styles.copy}>© {year} Launchly. Todos los derechos reservados.</p>
      </div>
    </footer>
  );
};

export default Footer;
