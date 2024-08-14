<template>
  <div class="content">
    <div class="container-fluid">
      <div class="row">
        <div class="col-12">
          <card class="strpied-tabled-with-hover"
                body-classes="table-full-width table-responsive">
            <template slot="header">
              <h4 class="card-title">Gestión de Usuarios</h4>
              <p class="card-category">Aquí podrá realizar el CRUD de usuarios</p>
              <button @click="createUser" class="btn btn-primary">Crear Usuario</button>
            </template>
            <l-table v-if="!selectedUser && !showCreateForm" class="table-hover table-striped"
                     :columns="table1.columns"
                     :data="table1.data"
                     @edit="editUser"
                     @delete="confirmDeleteUser">
            </l-table>
          </card>
        </div>
      </div>
    </div>

    <!-- Formulario de creación -->
    <create-profile v-if="showCreateForm" @close="closeCreateForm" />

    <!-- Formulario de edición -->
    <edit-profile-form v-if="selectedUser" :user="selectedUser" @close="closeEditForm" @update="updateUser" />
  </div>
</template>

<script>
import axios from 'axios'
import LTable from 'src/components/Table.vue'
import Card from 'src/components/Cards/Card.vue'
import EditProfileForm from "@/pages/UserProfile/EditProfileForm.vue";
import CreateProfile from "@/pages/UserProfile/CreateProfile.vue"; // Importa el nuevo componente

const tableColumns = [
  'id',
  'username',
  'first_name',
  'last_name',
  'email',
  'edad',
  'cpf',
  'is_active',
  'is_staff',

];

export default {
  components: {
    LTable,
    Card,
    EditProfileForm,
    CreateProfile, // Registra el nuevo componente
  },
  data() {
    return {
      table1: {
        columns: [...tableColumns],
        data: []
      },
      selectedUser: null,
      showCreateForm: false, // Propiedad para controlar el formulario de creación
      errorMessage: ''
    }
  },
  created() {
    this.fetchTableData()
  },
  methods: {
    async fetchTableData() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:8000/api/usuarios/', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        this.table1.data = response.data.results || response.data;
      } catch (error) {
        console.error('Error al obtener los datos:', error);
        this.errorMessage = 'Error al obtener los datos';
        if (error.response && error.response.status === 401) {
          this.errorMessage = 'No autorizado. Por favor, inicia sesión nuevamente.';
        }
        setTimeout(() => {
          this.errorMessage = '';
        }, 5000);
      }
    },
    createUser() {
      this.showCreateForm = true; // Muestra el formulario de creación
      this.selectedUser = null; // Muestra el formulario de creación
    },
    closeCreateForm() {
      this.showCreateForm = false; // Cierra el formulario de creación
      this.fetchTableData();
    },
    editUser(id) {
      const user = this.table1.data.find(user => user.id === id);
      if (user) {
        this.selectedUser = {...user};
      }
    },
    closeEditForm() {
      this.selectedUser = null;
      this.fetchTableData(); // Actualiza la tabla después de la edición
    },
    confirmDeleteUser(item) {
      if (confirm(`¿Estás seguro de que deseas eliminar al usuario?: ${item.id}`)) {
        this.deleteUser(item);
      }
    },
    deleteUser(item) {
      console.log('Eliminar usuario con ID:', item.id);
      const token = localStorage.getItem('token');
      axios.delete(`http://127.0.0.1:8000/api/usuarios/${item.id}/`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }).then(() => {
        this.fetchTableData();
      }).catch(error => {
        console.error('Error al eliminar el usuario:', error);
      });
    },
    async updateUser(updatedUser) {
      try {
        const token = localStorage.getItem('token');
        await axios.put(`http://127.0.0.1:8000/api/usuarios/${updatedUser.id}/`, updatedUser, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        this.fetchTableData(); // Actualiza la tabla después de la edición
        this.closeEditForm(); // Cierra el formulario de edición
      } catch (error) {
        console.error('Error al actualizar el usuario:', error);
        this.errorMessage = 'Error al actualizar el usuario';
        setTimeout(() => {
          this.errorMessage = '';
        }, 5000);
      }
    }
  }
}
</script>

<style>
</style>
