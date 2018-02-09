<template>
  <!--<div id="app">-->
  <div class="container">
    <!--UPLOAD-->
    <form enctype="multipart/form-data" novalidate v-if="isInitial || isSaving">
      <h1>Upload you csv files</h1>
      <div class="dropbox">
        <input type="file" multiple :name="uploadFieldName" :disabled="isSaving"
               @change="filesChange($event.target.files); fileCount = $event.target.files.length"
               accept="text/csv" class="input-file">
        <p v-if="isInitial">
          Drag your file(s) here to begin<br> or click to browse
        </p>
        <p v-if="isSaving">
          Uploading {{ fileCount }} files...
        </p>
      </div>
    </form>
    <!--SUCCESS-->
    <div v-if="isSuccess">
      <h2>Uploaded {{ uploadedFiles.length }} file(s) successfully.</h2>
      <p>
        <a href="javascript:void(0)" @click="reset()">Upload again</a>
      </p>
      <ul class="list-unstyled">
        <li v-for="item in uploadedFiles">
          <img :src="item.url" class="img-responsive img-thumbnail" :alt="item.originalName">
        </li>
      </ul>
    </div>
    <!--FAILED-->
    <div v-if="isFailed">
      <h2>Uploaded failed.</h2>
      <p>
        <a href="javascript:void(0)" @click="reset()">Try again</a>
      </p>
      <pre>{{ uploadError }}</pre>
    </div>
  </div>
  <!--</div>-->
</template>

<script>
  // import { upload } from './file-upload.service';

  const STATUS_INITIAL = 0, STATUS_SAVING = 1, STATUS_SUCCESS = 2, STATUS_FAILED = 3;

  export default {

    data() {
      return {
        uploadedFiles: [],
        uploadError: null,
        currentStatus: null,
        uploadFieldName: 'photos'
      }
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
      }
    },
    methods: {
      reset() {
        // reset form to initial state
        this.currentStatus = STATUS_INITIAL;
        this.uploadedFiles = [];
        this.uploadError = null;
      },
      //    upload(formData) {
      //   //if errors or cube constrcution probs don't show facts
      //   let url = 'cubes/add';
      //   this.$http.post(url, formData)
      //     .then(response => {
      //       console.log(response);
      //       console.log(formData);
      //       return response.data;
      //     });
      //
      //   // .then(data => {
      //   //   this.facts = data;
      //   // })
      // }
      // ,
      save(formData) {
        // upload data to the server
        this.currentStatus = STATUS_SAVING;
        let url = 'cubes/add';
        this.$http.post(url, {data : formData})

          .then(x => x.data)
          .then(x => {
            this.uploadedFiles = [].concat(x);
            this.currentStatus = STATUS_SUCCESS;
          })
          .catch(err => {
            this.uploadError = err.response;
            this.currentStatus = STATUS_FAILED;
          });
      },
      filesChange(fileList) {
        // handle file changes
        const formData = new FormData();
        if (!fileList.length) return;

        // append the files to FormData
        Array.from(Array(fileList.length).keys()).map(x => {
          formData.append(fileList[x], fileList[x].name);
        });
        // save it
        this.save(formData);
      }
    },
    mounted() {
      this.reset();
    },
  }
</script>

<style lang="scss" scoped>

  .dropbox {
    outline: 2px dashed grey; /* the dash box */
    outline-offset: -10px;
    background: lightcyan;
    color: dimgray;
    padding: 10px 10px;
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
  }

</style>
