<template>
  <div>
    <table style="width:100%">
      <tr>
        <td>
          <select class="form-control" v-model="engine" id="db-engine">
            <option disabled value="">Engine</option>
            <option>Postgres</option>
            <option>Mysql</option>
            <option>Oracle</option>
            <option>SQL Server</option>
          </select>

          <input
            class="form-control"
            placeholder="Server Name"
            type="text"
            v-model="servername"
            id="servername"
            name="servername"
          />

          <input
            class="form-control"
            placeholder="Port"
            type="text"
            v-model="port"
            name="port"
            id="port"
          />

          <input
            class="form-control"
            placeholder="User Name"
            type="text"
            v-model="username"
            name="username"
            id="username"
          />

          <input
            class="form-control"
            placeholder="Password"
            type="text"
            v-model="password"
            name="password"
            id="password"
          />

          <input
            class="btn-info"
            type="button"
            value="Connect"
            id="show-databases-btn"
            @click="connectDB()"
          />

          <div v-if="establishedConnection !== ''">
            Connection : {{ establishedConnection }}
          </div>
        </td>
        <td>
          <div v-if="establishedConnection.toUpperCase() === 'SUCCESS'">
            Available databases :
            <div
              class="available-databases"
              v-for="(database, index) in loadedDatabases"
              :key="database + index"
            >
              <label>
                <input
                  type="radio"
                  :key="index"
                  :id="database"
                  :value="database"
                  v-model="selectedDatabase"
                  @change="getCubeInfos($event)"
                />
                <label :for="database">{{ database }}</label> <br />
              </label>
            </div>
          </div>
          <!--
            <span v-if="selectedDatabase !== ''">selected : {{selectedDatabase}}</span>
          -->
        </td>
      </tr>
    </table>

    <br />
  </div>
</template>

<script>
import axios from "axios";
import { eventModalBus } from "../base-add-cube.vue";

export default {
  data: function() {
    return {
      engine: "postgres",
      servername: "localhost",
      port: "5432",
      username: "postgres",
      password: "root",
      loadedDatabases: [],
      establishedConnection: "",
      selectedDatabase: "",
    };
  },
  methods: {
    connectDB() {
      axios
        .post("api/cubes/connectDB", {
          engine: this.engine,
          servername: this.servername,
          port: this.port,
          username: this.username,
          password: this.password,
        })
        .then(response => {
          this.loadedDatabases = response.data;
          this.establishedConnection = "Success";
          this.$emit("SelectInputStatus", "toConfig");
        })
        .catch(() => {
          this.selectedDatabase = "";
          this.establishedConnection = "Failed";
        });
    },

    getCubeInfos(event) {
      const data = {
        selectCube: event.target.value,
        engine: this.engine,
        servername: this.servername,
        port: this.port,
        username: this.username,
        password: this.password,
      };
      axios
        .post("api/cubes/add_DB_cube", data)
        .then(response => {
          if (response.data.facts != null) {
            this.$emit("SelectInputStatus", "success");
          } else {
            this.$emit("SelectInputStatus", "toConfig");
          }
          eventModalBus.cubeConstructed(response.data);
          eventModalBus.ConnectionConfig(data);
        })
        .catch(() => {
          this.$emit("SelectInputStatus", "failed");
        });
    },
  },
  created() {
    eventModalBus.ConnectionConfig("");
  },
};
</script>

<style scoped>
.available-databases {
  margin-left: 10px;
}
</style>
