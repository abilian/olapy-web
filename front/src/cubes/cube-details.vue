<template>
  details
  [[ name ]]
  [[ description ]]
  [[ path ]]
</template>

<script>
  export default {
    name: "CubeDetail",
    data: function () {
      return {
        name : "my_cube" ,
        description : "description",
        path : "my path"
      };
    },

  }
</script>

<style scoped>

</style>
