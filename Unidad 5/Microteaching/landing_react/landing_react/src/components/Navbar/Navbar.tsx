import styles from './Navbar.module.css';

const links = [
  { label: 'Inicio', href: '#banner' },
  { label: 'Características', href: '#features' },
  { label: 'Contacto', href: '#contact' },
];

const  Navbar = () => {
  return (
    <header className={styles.navbar}>
      <div className={styles.inner}>
        <div className={styles.logo}>
          launch<span>ly</span>
        </div>
        <nav className={styles.nav}>
          {links.map((link) => (
            <a key={link.href} href={link.href} className={styles.navLink}>
              {link.label}
            </a>
          ))}
          <a href="#contact" className={styles.cta}>
            Empezar
          </a>
        </nav>
      </div>
    </header>
  );
};

export default Navbar;
