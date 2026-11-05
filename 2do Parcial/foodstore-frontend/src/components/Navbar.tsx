export function Navbar() {
    return (
        <header className="border-b border-gray-200 bg-white">
            <div className="mx-auto flex max-w-7xl items-center gap-4 px-4 py-4">
                <img
                    src="/food-icon.svg"
                    alt="Food Store"
                    className="h-10 w-10"
                />

                <div>
                    <h1 className="text-xl font-bold text-gray-900">
                        Food Store
                    </h1>

                    <p className="text-sm text-gray-600">
                        Administración de productos
                    </p>
                </div>

            </div>
        </header>
    )
}