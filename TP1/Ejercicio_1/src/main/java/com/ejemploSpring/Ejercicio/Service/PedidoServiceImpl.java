package com.ejemploSpring.Ejercicio.Service;

import com.ejemploSpring.Ejercicio.dtos.detallePedido.DetallePedidoCreate;
import com.ejemploSpring.Ejercicio.dtos.pedido.PedidoEdit;
import com.ejemploSpring.Ejercicio.entities.Pedido;
import com.ejemploSpring.Ejercicio.entities.Producto;
import com.ejemploSpring.Ejercicio.repository.PedidoRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class PedidoServiceImpl implements PedidoService {

    private final PedidoRepository pedidoRepository;
    private final ProductoService productoService;

    @Override
    public Pedido save(PedidoEdit pedidoEdit, List<DetallePedidoCreate> detalles) {

        Pedido pedido = Pedido.builder()
                .fecha(pedidoEdit.fecha())
                .estado(pedidoEdit.estado())
                .formapago(pedidoEdit.formaPago())
                .build();

        // Agregar detalles
        for (DetallePedidoCreate d : detalles) {
            Producto producto = productoService.findById(d.productoId());

            pedido.addDetallePedido(d.cantidad(), producto);
        }

        // Calcular total
        pedido.calcularTotal();

        return pedidoRepository.save(pedido);
    }

    @Override
    public Pedido findById(Long id) {
        return pedidoRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Pedido no encontrado"));
    }

    @Override
    public List<Pedido> findAll() {
        return pedidoRepository.findAll();
    }

    @Override
    public Pedido update(Long id, PedidoEdit pedidoEdit) {
        Pedido pedido = findById(id);

        pedido.setFecha(pedidoEdit.fecha());
        pedido.setEstado(pedidoEdit.estado());
        pedido.setFormapago(pedidoEdit.formaPago());

        pedido.calcularTotal();

        return pedidoRepository.save(pedido);
    }

    @Override
    public void delete(Long id) {
        pedidoRepository.deleteById(id);
    }
}