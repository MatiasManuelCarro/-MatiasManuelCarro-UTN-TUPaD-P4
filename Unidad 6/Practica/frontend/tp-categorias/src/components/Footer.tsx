function Footer() {
    return (
        <footer className="w-full h-14 flex items-center justify-center bg-linear-to-b from-[#5524B7] to-[#380B60] text-white/80">
            <div className="flex items-center gap-3">
                <img src="/icon_white.svg" alt="logo" className="w-6 h-6 opacity-90" />
                <span className="text-sm font-outfit tracking-wide">
                    Realizado por Matías Manuel Carro
                </span>
            </div>
        </footer>
    );
}

export default Footer;
