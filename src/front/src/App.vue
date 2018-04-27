<template>
  <div class="container">
    <div class="row">
      <div class="col-xs-12">
        <app-cubes/>
        <app-schema-options/>
        <app-schema-props/>
      </div>
    </div>
  </div>
</template>


<script>
import Cubes from "./cubes/the-cubes-names.vue";
import SchemaOptions from "./cubes/base-schema-options";
import SchemaProps from "./cubes/the-schema-props";

export default {
  delimiters: ["[[", "]]"],
  components: {
    appCubes: Cubes,
    appSchemaOptions: SchemaOptions,
    appSchemaProps: SchemaProps,
  },
};
</script>

<style>
</style>
