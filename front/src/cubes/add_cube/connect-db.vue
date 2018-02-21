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
        <input type="text" v-model="servername" name="servername">
      </label>
      <br>

      <label>
        Port :
        <input type="text" v-model="port" name="servername">
      </label>
      <br>

      <label>
        Database :
        <input type="text" v-model="database" name="servername">
      </label>
      <br>

      <label>
        User Name :
        <input type="text" v-model="username" name="servername">
      </label>
      <br>

      <label>
        Password :
        <input type="text" v-model="password" name="servername">
      </label>
      <br>

      <label>
        Connect :
        <input type="button" value="Connect" @click="connectDB()">
      </label>

      <div v-if="establishedConnection !== ''">
        Connection : {{establishedConnection}}
      </div>

      <div v-if="establishedConnection.toUpperCase() === 'SUCCESS'">
        Available databases :
        <div v-for="database in loadedDatabases">
          <label>
            <input type="radio" :id="database" :value="database" v-model="selectedDatabase">
            <label :for="database">{{database}}</label>
            <br>

          </label>
        </div>
        select : {{selectedDatabase}}
      </div>


      <br>
    </div>

  </div>

</template>

<script>
  export default {
    data: function () {
      return {
        engine: 'postgres',
        servername: 'localhost',
        port: '5432',
        database: 'tutorial',
        username: 'postgres',
        password: 'root',
        loadedDatabases: [],
        establishedConnection: '',
        selectedDatabase: ''

      }
    },
    methods: {
      connectDB() {
        this.$http.post('cubes/connectDB', {
          'engine': this.engine,
          'servername': this.servername,
          'port': this.port,
          'database': this.database,
          'username': this.username,
          'password': this.password

        }).then(x => {
          this.loadedDatabases = x.data;
          this.establishedConnection = 'Success';
        })
          .catch(x => {
            this.establishedConnection = 'Failed';
          })

      }
    }
  }
</script>

<style scoped>

</style>
