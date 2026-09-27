import styles from './Features.module.css';
import FeatureCard from './FeatureCard';

interface Feature {
  icon: string;
  title: string;
  description: string;
}

const features: Feature[] = [
  {
    icon: '⚡',
    title: 'Rendimiento',
    description: 'Infraestructura optimizada con tiempos de respuesta rápidos para que tu producto siempre funcione bien.',
  },
  {
    icon: '🔒',
    title: 'Seguridad',
    description: 'Cifrado y autenticación incluidos. Tus datos y los de tus usuarios siempre protegidos.',
  },
  {
    icon: '📊',
    title: 'Analíticas',
    description: 'Métricas claras para entender cómo usan tu producto y tomar mejores decisiones.',
  },
  {
    icon: '🔗',
    title: 'Integraciones',
    description: 'Conéctate fácilmente con las herramientas que ya usas como Slack, Notion y Stripe.',
  },
  {
    icon: '🤖',
    title: 'Automatización',
    description: 'Automatiza tareas repetitivas y enfoca a tu equipo en lo que realmente importa.',
  },
  {
    icon: '🌍',
    title: 'Global',
    description: 'Disponible en múltiples regiones del mundo para que tus usuarios tengan la mejor experiencia.',
  },
];

const Features = () => {
  return (
    <section id="features" className={styles.features}>
      <div className={styles.inner}>
        <div className={styles.header}>
          <h2 className={styles.title}>Todo lo que necesitas</h2>
          <p className={styles.subtitle}>
            Diseñado para equipos que quieren avanzar rápido.
          </p>
        </div>
        <div className={styles.grid}>
          {features.map((feature) => (
            <FeatureCard
              key={feature.title}
              icon={feature.icon}
              title={feature.title}
              description={feature.description}
            />
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;
