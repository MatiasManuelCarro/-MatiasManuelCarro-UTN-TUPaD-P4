import Navbar from "../../components/Navbar/Navbar";
import Banner from "../../components/Banner/Banner";
import Features from "../../components/Features/Features";
import ContactForm from "../../components/ContactForm/ContactForm";
import Footer from "../../components/Footer/Footer";

const LandingPage = () => {
    return (
        <>
            <Navbar />
            <main>
                <Banner />
                <Features />
                <ContactForm />
            </main>
            <Footer />
        </>
    );
};

export default LandingPage; 