<template>

  <div>
    <div style="position: center">
      <label>
        engine :
        <select v-model="engine">
          <option disabled value="">Choisissez</option>
          <option>Postgres</option>
          <option>Mysql</option>
          <option>Oracle</option>
          <option>SQL Server</option>
        </select>
      </label>
      <br>

      <label>
        Server Name :
        <input type="text" :value="servername" name="servername">
      </label>
      <br>

      <label>
        Port :
        <input type="text" :value="port" name="servername">
      </label>
      <br>

      <label>
        Database :
        <input type="text" :value="database" name="servername">
      </label>
      <br>

      <label>
        User Name :
        <input type="text" :value="username" name="servername">
      </label>
      <br>

      <label>
        Password :
        <input type="text" :value="password" name="servername">
      </label>
      <br>
    </div>

  </div>

</template>

<script>
  export default {
    data: function () {
      return {
        engine: '',
        servername: 'localhost',
        port: '',
        database: '',
        username: '',
        password: '',

      }
    }
  }
</script>

<style scoped>

</style>
