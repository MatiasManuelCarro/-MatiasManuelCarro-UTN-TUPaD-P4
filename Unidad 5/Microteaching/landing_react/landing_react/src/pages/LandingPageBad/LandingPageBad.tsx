import navbarStyles from '../../components/Navbar/Navbar.module.css';
import bannerStyles from '../../components/Banner/Banner.module.css';
import featuresStyles from '../../components/Features/Features.module.css';
import contactStyles from '../../components/ContactForm/ContactForm.module.css';
import footerStyles from '../../components/Footer/Footer.module.css';

const LandingPageBad = () => {
  const year = new Date().getFullYear();

  return (
    <>
      {/* ===== NAVBAR ===== */}
      <header className={navbarStyles.navbar}>
        <div className={navbarStyles.inner}>
          <div className={navbarStyles.logo}>
            launch<span>ly</span>
          </div>
          <nav className={navbarStyles.nav}>
            <a href="#banner" className={navbarStyles.navLink}>Inicio</a>
            <a href="#features" className={navbarStyles.navLink}>Características</a>
            <a href="#contact" className={navbarStyles.navLink}>Contacto</a>
            <a href="#contact" className={navbarStyles.cta}>Empezar</a>
          </nav>
        </div>
      </header>

      {/* ===== BANNER ===== */}
      <section id="banner" className={bannerStyles.banner}>
        <div className={bannerStyles.inner}>
          <h1 className={bannerStyles.title}>
            La plataforma que impulsa tu negocio
          </h1>
          <p className={bannerStyles.subtitle}>
            Herramientas modernas para equipos ambiciosos. Lanza más rápido y
            escala sin preocuparte por la infraestructura.
          </p>
          <div className={bannerStyles.actions}>
            <a href="#contact" className={bannerStyles.btnPrimary}>
              Empezar gratis
            </a>
            <a href="#features" className={bannerStyles.btnSecondary}>
              Ver características
            </a>
          </div>
        </div>
      </section>

      {/* ===== FEATURES ===== */}
      <section id="features" className={featuresStyles.features}>
        <div className={featuresStyles.inner}>
          <div className={featuresStyles.header}>
            <h2 className={featuresStyles.title}>Todo lo que necesitas</h2>
            <p className={featuresStyles.subtitle}>
              Diseñado para equipos que quieren avanzar rápido.
            </p>
          </div>
          <div className={featuresStyles.grid}>
            <div className={featuresStyles.card}>
              <div className={featuresStyles.icon}>⚡</div>
              <h3 className={featuresStyles.cardTitle}>Rendimiento</h3>
              <p className={featuresStyles.cardDesc}>
                Infraestructura optimizada con tiempos de respuesta rápidos para que tu producto siempre funcione bien.
              </p>
            </div>
            <div className={featuresStyles.card}>
              <div className={featuresStyles.icon}>🔒</div>
              <h3 className={featuresStyles.cardTitle}>Seguridad</h3>
              <p className={featuresStyles.cardDesc}>
                Cifrado y autenticación incluidos. Tus datos y los de tus usuarios siempre protegidos.
              </p>
            </div>
            <div className={featuresStyles.card}>
              <div className={featuresStyles.icon}>📊</div>
              <h3 className={featuresStyles.cardTitle}>Analíticas</h3>
              <p className={featuresStyles.cardDesc}>
                Métricas claras para entender cómo usan tu producto y tomar mejores decisiones.
              </p>
            </div>
            <div className={featuresStyles.card}>
              <div className={featuresStyles.icon}>🔗</div>
              <h3 className={featuresStyles.cardTitle}>Integraciones</h3>
              <p className={featuresStyles.cardDesc}>
                Conéctate fácilmente con las herramientas que ya usas como Slack, Notion y Stripe.
              </p>
            </div>
            <div className={featuresStyles.card}>
              <div className={featuresStyles.icon}>🤖</div>
              <h3 className={featuresStyles.cardTitle}>Automatización</h3>
              <p className={featuresStyles.cardDesc}>
                Automatiza tareas repetitivas y enfoca a tu equipo en lo que realmente importa.
              </p>
            </div>
            <div className={featuresStyles.card}>
              <div className={featuresStyles.icon}>🌍</div>
              <h3 className={featuresStyles.cardTitle}>Global</h3>
              <p className={featuresStyles.cardDesc}>
                Disponible en múltiples regiones del mundo para que tus usuarios tengan la mejor experiencia.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* ===== CONTACT FORM ===== */}
      <section id="contact" className={contactStyles.section}>
        <div className={contactStyles.inner}>
          <div className={contactStyles.info}>
            <h2 className={contactStyles.title}>¿Tienes alguna pregunta?</h2>
            <p className={contactStyles.subtitle}>
              Completá el formulario y nos ponemos en contacto contigo en menos de 24 horas.
            </p>
          </div>
          <form className={contactStyles.form}>
            <div className={contactStyles.row}>
              <div className={contactStyles.field}>
                <label className={contactStyles.label} htmlFor="firstName">Nombre</label>
                <input
                  className={contactStyles.input}
                  id="firstName"
                  name="firstName"
                  type="text"
                  placeholder="Juan"
                  required
                />
              </div>
              <div className={contactStyles.field}>
                <label className={contactStyles.label} htmlFor="lastName">Apellido</label>
                <input
                  className={contactStyles.input}
                  id="lastName"
                  name="lastName"
                  type="text"
                  placeholder="García"
                  required
                />
              </div>
            </div>
            <div className={contactStyles.field}>
              <label className={contactStyles.label} htmlFor="email">Email</label>
              <input
                className={contactStyles.input}
                id="email"
                name="email"
                type="email"
                placeholder="juan@empresa.com"
                required
              />
            </div>
            <div className={contactStyles.field}>
              <label className={contactStyles.label} htmlFor="message">Mensaje</label>
              <textarea
                className={contactStyles.textarea}
                id="message"
                name="message"
                placeholder="Escribí tu mensaje..."
                required
              />
            </div>
            <button type="submit" className={contactStyles.submit}>
              Enviar mensaje
            </button>
          </form>
        </div>
      </section>

      {/* ===== FOOTER ===== */}
      <footer className={footerStyles.footer}>
        <div className={footerStyles.top}>
          <div>
            <p className={footerStyles.logo}>Launchly</p>
            <p className={footerStyles.brandDesc}>
              La plataforma para equipos que quieren construir grandes productos.
            </p>
          </div>
          <div>
            <p className={footerStyles.colTitle}>Producto</p>
            <ul className={footerStyles.colLinks}>
              <li><a href="#">Características</a></li>
              <li><a href="#">Precios</a></li>
              <li><a href="#">Changelog</a></li>
              <li><a href="#">Roadmap</a></li>
            </ul>
          </div>
          <div>
            <p className={footerStyles.colTitle}>Empresa</p>
            <ul className={footerStyles.colLinks}>
              <li><a href="#">Sobre nosotros</a></li>
              <li><a href="#">Blog</a></li>
              <li><a href="#">Prensa</a></li>
              <li><a href="#">Careers</a></li>
            </ul>
          </div>
          <div>
            <p className={footerStyles.colTitle}>Soporte</p>
            <ul className={footerStyles.colLinks}>
              <li><a href="#">Documentación</a></li>
              <li><a href="#">API</a></li>
              <li><a href="#">Comunidad</a></li>
              <li><a href="#">Contacto</a></li>
            </ul>
          </div>
        </div>
        <div className={footerStyles.bottom}>
          <p className={footerStyles.copy}>© {year} Launchly. Todos los derechos reservados.</p>
        </div>
      </footer>
    </>
  );
};

export default LandingPageBad;
