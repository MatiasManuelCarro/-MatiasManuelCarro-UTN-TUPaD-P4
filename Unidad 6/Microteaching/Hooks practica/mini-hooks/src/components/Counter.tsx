import { useState, useEffect } from "react"

function Counter() {
    const [count, setCount] = useState<number>(0)

    // Efecto: log al montar
    useEffect(() => {
        console.log("Counter montado")
    }, [])

    // Efecto: log cuando cambia count
    useEffect(() => {
        console.log("El contador cambió:", count)
    }, [count])

    // Event listener: Enter incrementa el contador
    useEffect(() => {
        const handler = (e: KeyboardEvent) => {
            if (e.key === "Enter") {
                setCount(prev => prev + 1)
            }
        }

        document.addEventListener("keydown", handler)

        return () => {
            document.removeEventListener("keydown", handler)
        }
    }, [])


    return (
        <div>
            <p>Valor actual: {count}</p>
            <button onClick={() => setCount(count + 1)}>
                Incrementar con click
            </button>
            <p>También podés presionar Enter para sumar.</p>
        </div>
    )
}

export default Counter
