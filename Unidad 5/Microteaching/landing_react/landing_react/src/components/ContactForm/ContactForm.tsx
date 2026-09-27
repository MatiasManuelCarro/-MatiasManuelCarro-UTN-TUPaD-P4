import styles from './ContactForm.module.css';


const ContactForm = () => {
  

  return (
    <section id="contact" className={styles.section}>
      <div className={styles.inner}>
        <div className={styles.info}>
          <h2 className={styles.title}>¿Tienes alguna pregunta?</h2>
          <p className={styles.subtitle}>
            Completá el formulario y nos ponemos en contacto contigo en menos de
            24 horas.
          </p>
        </div>

        
          <form className={styles.form}>
            <div className={styles.row}>
              <div className={styles.field}>
                <label className={styles.label} htmlFor="firstName">Nombre</label>
                <input
                  className={styles.input}
                  id="firstName"
                  name="firstName"
                  type="text"
                  placeholder="Juan"
                  
                  required
                />
              </div>
              <div className={styles.field}>
                <label className={styles.label} htmlFor="lastName">Apellido</label>
                <input
                  className={styles.input}
                  id="lastName"
                  name="lastName"
                  type="text"
                  placeholder="García"
                  
                  required
                />
              </div>
            </div>

            <div className={styles.field}>
              <label className={styles.label} htmlFor="email">Email</label>
              <input
                className={styles.input}
                id="email"
                name="email"
                type="email"
                placeholder="juan@empresa.com"
                
                required
              />
            </div>

            <div className={styles.field}>
              <label className={styles.label} htmlFor="message">Mensaje</label>
              <textarea
                className={styles.textarea}
                id="message"
                name="message"
                placeholder="Escribí tu mensaje..."
                
                required
              />
            </div>

            <button type="submit" className={styles.submit}>
              Enviar mensaje
            </button>
          </form>
        
      </div>
    </section>
  );
};

export default ContactForm;
