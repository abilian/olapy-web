<template>
  <div class="container">
    <div class="row">
      <div class="col-xs-12">
        <app-cubes></app-cubes>
        <app-schema-options></app-schema-options>
        <app-schema-props></app-schema-props>
      </div>
    </div>
  </div>
</template>


<script>
  import Cubes from './cubes/cubes-names.vue';
  import SchemaOptions from './cubes/schema-options';
  import SchemaProps from './cubes/schema-props';

  export default {
    delimiters: ['[[', ']]'],
    components: {
      appCubes: Cubes,
      appSchemaOptions: SchemaOptions,
      appSchemaProps: SchemaProps
    },
  }

</script>

<style>
</style>
