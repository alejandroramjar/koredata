<template>
  <div v-if="isVisible" class="modal-overlay">
    <div class="modal">
      <h3>Confirmar Eliminación</h3>
      <p>¿Estás seguro de que deseas eliminar al siguiente usuario?</p>
      <ul v-if="user && Object.keys(user).length">
        <li>ID: {{ user.id }}</li>
        <li>Usuario: {{ user.username }}</li>
        <li>Correo: {{ user.email }}</li>
        <!-- Agrega más campos según sea necesario -->
      </ul>
      <p v-else>No hay datos del usuario.</p>
      <button @click="confirmDelete" class="btn btn-danger">Eliminar</button>
      <button @click="cancelDelete" class="btn btn-secondary">Cancelar</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Modal',
  props: {
    isVisible: {
      type: Boolean,
      required: true
    },
    user: {
      type: Object,
      required: true
    }
  },
  methods: {
    confirmDelete() {
      this.$emit('confirm');
    },
    cancelDelete() {
      this.$emit('cancel');
    }
  }
}
</script>

<style>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  background: white;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
</style>
