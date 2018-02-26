<template>

  <div>
    <table style="width:100%">
      <tr>
        <td>
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
        </td>
        <td>
          <div v-if="establishedConnection.toUpperCase() === 'SUCCESS'">
            Available databases :
            <div v-for="database in loadedDatabases">
              <label>
                <input type="radio" :id="database" :value="database" v-model="selectedDatabase"
                       @change="getCubeInfos($event)">
                <label :for="database">{{database}}</label>
                <br>
              </label>
            </div>
          </div>
          <span v-if="selectedDatabase !== ''">selected : {{selectedDatabase}}</span>
        </td>
      </tr>
    </table>
    <br>

  </div>

</template>

<script>

  import {eventModalBus} from '../schema-options.vue';


  export default {
    data: function () {
      return {
        engine: 'postgres',
        servername: 'localhost',
        port: '5432',
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
          'username': this.username,
          'password': this.password

        }).then(x => {
          this.loadedDatabases = x.data;
          this.establishedConnection = 'Success';
          this.$emit('SelectInputStatus', 'toConfig');

        })
          .catch(x => {
            this.selectedDatabase = '';
            this.establishedConnection = 'Failed';
          })

      },
      getCubeInfos(event) {
        let data = {
          'selectCube': event.target.value,
          'engine': this.engine,
          'servername': this.servername,
          'port': this.port,
          'username': this.username,
          'password': this.password

        };
        this.$http.post('cubes/add_DB_cube', data)
          .then(x => {
            if (x.data.facts != null) {
              this.$emit('SelectInputStatus', 'success');
            }
            else {
              this.$emit('SelectInputStatus', 'toConfig');
            }
            eventModalBus.cubeConstructed(x.data);
            eventModalBus.ConnectionConfig(data);
          })
          .catch(err => {
            this.$emit('SelectInputStatus', 'failed');
          });
      }
    },
    created() {
      eventModalBus.ConnectionConfig('');
    }
  }
</script>

<style scoped>

</style>
