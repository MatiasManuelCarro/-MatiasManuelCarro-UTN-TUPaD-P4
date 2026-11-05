export function Footer() {
    return (
        <footer className="border-t border-gray-200 bg-white">
            <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-4">
                <div>
                    <p className="text-sm font-medium text-gray-900">
                        Pagina desarrollada por: Matias Manuel Carro
                    </p>
                    <p className="text-xs text-gray-500">Programación IV</p>
                </div>
                <img src="/UTN.svg" alt="UTN" className="h-10 w-auto" />
            </div>
        </footer>
    );
}
