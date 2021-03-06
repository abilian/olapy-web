<template>
  <div class="container">
    <!-- UPLOAD -->
    <form enctype="multipart/form-data" novalidate v-if="isInitial || isSaving">
      <!-- <h1>Upload csv files</h1> -->
      <div class="dropbox">
        <input
          type="file"
          multiple
          :name="uploadFieldName"
          :disabled="isSaving"
          @change="
            filesChange($event.target.name, $event.target.files);
            fileCount = $event.target.files.length;
          "
          accept="text/csv"
          class="input-file"
        />
        <p v-if="isInitial">
          Drag your file(s) here to begin<br />
          or click to browse
        </p>
        <p v-if="isSaving">Uploading {{ fileCount }} files...</p>
      </div>
    </form>
    <!-- SUCCESS -->
    <div v-if="isSuccess">
      <h2>Uploaded {{ uploadedFiles.length }} file(s) successfully.</h2>
      <p><a href="javascript:void(0)" @click="reset()">Upload again</a></p>
      <ul class="list-unstyled">
        <li v-for="(item, index) in uploadedFiles" :key="item + index">
          {{ index }} - {{ item }}
        </li>
        <!-- <li v-for="item in uploadedFiles"> -->
        <!--
          <img :src="item.url" class="img-responsive img-thumbnail" :alt="item.originalName">
        -->
        <!--
          &lt;!&ndash;<img :src="item.url" class="img-responsive img-thumbnail" :alt="item.originalName">&ndash;&gt;
        -->
        <!-- </li> -->
      </ul>
    </div>
    <!-- FAILED -->
    <div v-if="isFailed">
      <h2>Uploaded failed.</h2>
      <p><a href="javascript:void(0)" @click="reset()">Try again</a></p>
      <pre>{{ uploadError }}</pre>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { eventModalBus } from "../base-add-cube.vue";

const STATUS_INITIAL = 0;
const STATUS_SAVING = 1;
const STATUS_SUCCESS = 2;
const STATUS_FAILED = 3;

export default {
  props: {
    newCubeName: String,
  },

  data() {
    return {
      uploadedFiles: [],
      uploadError: null,
      currentStatus: null,
      uploadFieldName: "files",
    };
  },

  computed: {
    isInitial() {
      return this.currentStatus === STATUS_INITIAL;
    },
    isSaving() {
      return this.currentStatus === STATUS_SAVING;
    },
    isSuccess() {
      return this.currentStatus === STATUS_SUCCESS;
    },
    isFailed() {
      return this.currentStatus === STATUS_FAILED;
    },
  },

  mounted() {
    this.reset();
  },

  methods: {
    reset() {
      // reset form to initial state
      this.currentStatus = STATUS_INITIAL;
      this.uploadedFiles = [];
      this.uploadError = null;
    },

    save(formData) {
      // upload data to the server
      this.currentStatus = STATUS_SAVING;
      axios
        .post("/api/cubes/add", formData)
        .then((response) => {
          this.uploadedFiles = [].concat(response.data.dimensions);
          if (response.data.facts != null) {
            this.uploadedFiles.push(response.data.facts);
            this.$emit("SelectInputStatus", "success");
          } else {
            this.$emit("SelectInputStatus", "toConfig");
          }
          eventModalBus.cubeConstructed(response.data);
          this.currentStatus = STATUS_SUCCESS;
        })
        .catch((err) => {
          this.uploadError = err.response;
          this.currentStatus = STATUS_FAILED;
          this.$emit("SelectInputStatus", "failed");
        });
    },

    filesChange(fieldName, fileList) {
      // handle file changes
      const formData = new FormData();

      if (!fileList.length) {
        return;
      }

      // append the files to FormData
      Array.from(Array(fileList.length).keys()).map((x) => {
        formData.append(fieldName, fileList[x], fileList[x].name);
      });

      // save it
      this.save(formData);
    },
  },
};
</script>

<style lang="scss" scoped>
.dropbox {
  outline: 2px dashed grey; /* the dash box */
  outline-offset: -10px;
  background: lightcyan;
  color: dimgray;
  /*padding: 10px 10px;*/
  min-height: 200px; /* minimum height */
  position: relative;
  cursor: pointer;
}

.input-file {
  opacity: 0; /* invisible but it's there! */
  width: 100%;
  height: 200px;
  position: absolute;
  cursor: pointer;
}

.dropbox:hover {
  background: lightblue; /* when mouse over to the drop zone, change color */
}

.dropbox p {
  font-size: 1.2em;
  text-align: center;
  padding: 50px 0;
}

.container {
  width: 100%;
  margin-top: 7px;
}
</style>
