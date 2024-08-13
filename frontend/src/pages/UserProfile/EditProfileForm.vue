<template>
  <card>
    <h4 slot="header" class="card-title text-center">Editar Perfil</h4>
    <form @submit.prevent="updateProfile">
      <div class="row mb-4">
        <div class="col-md-6">
          <base-input
            type="text"
            label="Nombre"
            placeholder="Nombre"
            v-model="user.first_name"
          />
        </div>
        <div class="col-md-6">
          <base-input
            type="text"
            label="Apellido"
            placeholder="Apellido"
            v-model="user.last_name"
          />
        </div>
      </div>

      <div class="row mb-4">
        <div class="col-md-3">
          <base-input
            type="text"
            label="Usuario"
            :disabled="true"
            placeholder="Usuario"
            v-model="user.username"
          />
        </div>
        <div class="col-md-3">
          <base-input
            type="text"
            label="CPF"
            placeholder="CPF"
            v-model="user.cpf"
          />
        </div>
        <div class="col-md-3">
          <base-input
            type="email"
            label="Email"
            placeholder="Email"
            v-model="user.email"
          />
        </div>
        <div class="col-md-3">
          <base-input
            type="number"
            label="Edad"
            placeholder="Edad"
            v-model="user.edad"
          />
        </div>
      </div>

      <div class="row mb-4 align-items-center">
        <div class="col-md-3">
          <base-checkbox
            :checked="user.is_active"
            @input="value => user.is_active = value"
          />
          Activo?
        </div>
      </div>

      <div class="text-center">
        <button type="submit" class="btn btn-info btn-fill">
          Actualizar Perfil
        </button>
        <button type="button" class="btn btn-secondary" @click="$emit('close')">
          Cancelar
        </button>
      </div>
    </form>
  </card>
</template>

<script>
import axios from 'axios'; // Asegúrate de importar axios

export default {
  props: {
    user: {
      type: Object,
      required: true
    }
  },
  methods: {
    updateProfile() {
      console.log(this.user); // Muestra el usuario en la consola
      const token = localStorage.getItem('token');
      axios.put(`http://127.0.0.1:8000/api/usuarios/${this.user.id}/`, this.user, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      .then(() => {
        alert('Perfil actualizado con éxito');
        this.$emit('close'); // Cerrar el formulario después de la actualización
      })
      .catch(error => {
        console.error('Error al actualizar el perfil:', error);
        alert('Error al actualizar el perfil');
      });
    }
  }
}
</script>

<style>
</style>
