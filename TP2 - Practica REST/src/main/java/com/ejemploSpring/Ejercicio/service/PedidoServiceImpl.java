package com.ejemploSpring.Ejercicio.service;

import com.ejemploSpring.Ejercicio.dtos.detallePedido.DetallePedidoCreate;
import com.ejemploSpring.Ejercicio.dtos.pedido.PedidoCreate;
import com.ejemploSpring.Ejercicio.dtos.pedido.PedidoEdit;
import com.ejemploSpring.Ejercicio.entities.Pedido;
import com.ejemploSpring.Ejercicio.entities.Producto;
import com.ejemploSpring.Ejercicio.entities.Usuario;
import com.ejemploSpring.Ejercicio.repository.DetallePedidoRepository;
import com.ejemploSpring.Ejercicio.repository.PedidoRepository;
import com.ejemploSpring.Ejercicio.repository.ProductoRepository;
import com.ejemploSpring.Ejercicio.repository.UsuarioRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
public class PedidoServiceImpl implements PedidoService {

    private final PedidoRepository pedidoRepository;
    private final ProductoService productoService;
    private final UsuarioRepository usuarioRepository;
    private final ProductoRepository productoRepository;
    private final DetallePedidoRepository detallePedidoRepository ;

    @Override
    public Pedido save(PedidoCreate pedidoCreate) {

        Pedido pedido = Pedido.builder()
                .fecha(pedidoCreate.fecha())
                .estado(pedidoCreate.estado())
                .formapago(pedidoCreate.formapago())
                .build();

        for (DetallePedidoCreate d : pedidoCreate.detalles()) {
            Producto producto = productoService.findEntityById(d.productoId());
            pedido.addDetallePedido(d.cantidad(), producto);
        }

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
        pedido.setFormapago(pedidoEdit.formapago());

        pedido.calcularTotal();

        return pedidoRepository.save(pedido);
    }

    @Override
    public void deleteById(Long id) { //Baja logica
        Pedido pedido = pedidoRepository.findById(id)
                .orElseThrow(() -> new NullPointerException("No se encontró pedido con id " + id));

        pedido.setEliminado(true);
        pedidoRepository.save(pedido);
    }


    @Transactional
    public void asignarPedido(Long usuarioId, Pedido pedido) {
        Usuario usuario = usuarioRepository.findById(usuarioId)
                .orElseThrow(() -> new RuntimeException("Usuario no encontrado"));

        usuario.addPedido(pedido);
    }

}