<template>
  <table class="table">
    <thead>
      <tr>
        <th v-for="column in columns" :key="column">{{ column }}</th>
        <th v-if="!columns.includes('Acciones')">Acciones</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(item, index) in data" :key="index">
        <td v-for="column in columns" :key="column">
          {{ itemValue(item, column) }}
        </td>
        <td>
          <button @click="$emit('edit', item.id)" class="btn btn-outline-warning">Editar</button>
          <button @click="$emit('delete', item)" class="btn btn-outline-danger">Eliminar</button>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: 'l-table',
  props: {
    columns: Array,
    data: Array
  },
  methods: {
    itemValue(item, column) {
      const key = column.toLowerCase(); // Ajusta según la clave
      return item[key] !== undefined ? item[key] : 'N/A'; // Manejo de valores no definidos
    }
  }
}
</script>

<style>
</style>
