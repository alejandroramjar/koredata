<template>
  <card>
    <h4 slot="header" class="card-title text-center">Crear Usuario</h4>
    <form @submit.prevent="createUser">
      <div class="row mb-4">
        <div class="col-md-6">
          <base-input
            type="text"
            label="Nombre"
            placeholder="Nombre"
            v-model="newUser.first_name"
          />
        </div>
        <div class="col-md-6">
          <base-input
            type="text"
            label="Apellido"
            placeholder="Apellido"
            v-model="newUser.last_name"
          />
        </div>
      </div>

      <div class="row mb-4">
        <div class="col-md-3">
          <base-input
            type="text"
            label="Usuario"
            placeholder="Usuario"
            v-model="newUser.username"
          />
        </div>
        <div class="col-md-3">
          <base-input
            type="text"
            label="CPF"
            placeholder="CPF"
            v-model="newUser.cpf"
          />
        </div>
        <div class="col-md-3">
          <base-input
            type="number"
            label="Edad"
            placeholder="Edad"
            v-model="newUser.edad"
          />
        </div>
        <div class="col-md-3">
          <base-input
            type="email"
            label="Email"
            placeholder="Email"
            v-model="newUser.email"
          />
        </div>
        <div class="col-md-3">
          <base-input
            type="password"
            label="Contraseña"
            placeholder="Contraseña"
            v-model="newUser.password"
          />
        </div>
        <div class="col-md-3">
          <base-input
            type="password"
            label="Repetir Contraseña"
            placeholder="Repetir Contraseña"
            v-model="newUser.password2"
          />
        </div>
      </div>

      <div class="row mb-4 align-items-center">
        <div class="col-md-3">
          <base-checkbox
            v-model="newUser.is_active"
          />
          Activo?
        </div>
      </div>

      <div v-if="passwordMismatch" class="text-danger">
        Las contraseñas no coinciden.
      </div>

      <div class="text-center">
        <button type="submit" class="btn btn-info btn-fill" :disabled="passwordMismatch">
          Crear Usuario
        </button>
        <button type="button" class="btn btn-secondary" @click="$emit('close')">
          Cancelar
        </button>
      </div>
    </form>
  </card>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      newUser: {
        first_name: '',
        last_name: '',
        username: '',
        cpf: '',
        email: '',
        password: '',
        password2: '',
        is_active: true // Valor por defecto
      },
      passwordMismatch: false,
    }
  },
  watch: {
    'newUser.password': function () {
      this.checkPasswordMismatch();
    },
    'newUser.password2': function () {
      this.checkPasswordMismatch();
    }
  },
  methods: {
    checkPasswordMismatch() {
      this.passwordMismatch = this.newUser.password !== this.newUser.password2;
    },
    createUser() {
      if (this.passwordMismatch) {
        alert('Las contraseñas no coinciden.'); // Asegúrate de que las contraseñas coincidan antes de enviar
        return;
      }
      const token = localStorage.getItem('token');
      axios.post('http://127.0.0.1:8000/api/registro/', this.newUser, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
        .then(() => {
          alert('Usuario creado con éxito');
          this.$emit('close'); // Cerrar el formulario después de la creación
        })
        .catch(error => {
          console.error('Error al crear el usuario:', error);
          alert('Error al crear el usuario');
        });
    }
  }
}
</script>

<style>
.text-danger {
  color: red;
}
</style>
