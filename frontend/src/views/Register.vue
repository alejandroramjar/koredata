<template>
  <div class="container mt-5">
    <div class="card shadow-sm">
      <div class="card-body">
        <h2 class="card-title text-center mb-4">Registrarse</h2>
        <form @submit.prevent="register">
          <div class="row mb-3">
            <div class="col">
              <label for="first_name" class="form-label">Nombre(s)</label>
              <input type="text" class="form-control" id="first_name" v-model="first_name" required>
            </div>
            <div class="col">
              <label for="last_name" class="form-label">Apellidos</label>
              <input type="text" class="form-control" id="last_name" v-model="last_name" required>
            </div>
          </div>
          <div class="row mb-3">
            <div class="col">
              <label for="username" class="form-label">Nombre de Usuario</label>
              <input type="text" class="form-control" id="username" v-model="username" required>
            </div>
            <div class="col">
              <label for="email" class="form-label">Correo Electrónico</label>
              <input type="email" class="form-control" id="email" v-model="email" required>
            </div>
          </div>
          <div class="row mb-3">
            <div class="col">
              <label for="edad" class="form-label">Edad</label>
              <input type="number" class="form-control" id="edad" v-model="edad">
            </div>
            <div class="col">
              <label for="cpf" class="form-label">cpf</label>
              <input type="number" class="form-control" id="cpf" v-model="cpf">
            </div>
          </div>
          <div class="row mb-3">
            <div class="col">
              <label for="password" class="form-label">Contraseña</label>
              <input type="password" class="form-control" id="password" v-model="password" required>
            </div>
            <div class="col">
              <label for="password2" class="form-label">Confirmar Contraseña</label>
              <input type="password" class="form-control" id="password2" v-model="password2" required>
            </div>
          </div>
          <div class="d-grid gap-2">
            <button type="submit" class="btn btn-outline-dark">Registrarse</button>
            <p class="text-center mt-3">
              ¿Ya tienes una cuenta?
              <router-link to="/login">Inicia sesión aquí</router-link>
            </p>


          </div>
        </form>
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  name: 'Register',
  data() {
    return {
      username: '',
      first_name: '',
      last_name: '',
      password: '',
      password2: '',
      email: '',
      edad: null,
      cpf: '',
    };
  },
  methods: {
    async register() {
      if (this.password !== this.password2) {
        alert("Las contraseñas no coinciden");
        return;
      }

      let formData = new FormData();
      formData.append('username', this.username);
      formData.append('first_name', this.first_name);
      formData.append('last_name', this.last_name);
      formData.append('password', this.password);
      formData.append('password2', this.password2);
      formData.append('email', this.email);
      formData.append('edad', this.edad);
      formData.append('cpf', this.cpf);

      try {
        const response = await axios.post('http://localhost:8000/api/registro/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        console.log(response);
        alert('Registro exitoso. Ahora puedes iniciar sesión.');
        this.$router.push('/login');
      } catch (error) {
        console.error(error);
        alert('Error en el registro');
      }
    },
    onFileChange(event) {
      this.image = event.target.files[0];
    }
  }
}
</script>


<style scoped>
.container {
  max-width: 400px;
}

.card {
  border-radius: 10px;
}

.card-title {
  font-weight: bold;
}

.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
}

.btn-secondary {
  background-color: #6c757d;
  border-color: #6c757d;
}
</style>
