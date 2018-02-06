<template>
  <div class="schema_props">
    <div class="cube_components">

      <button @click="selectedComponent = 'appCube'">Cube</button>
      <button @click="selectedComponent = 'appDimensions'">Dimensions</button>
      <button @click="selectedComponent = 'appFacts'">Facts</button>
      <keep-alive>
        <component :is="selectedComponent" :currentCube="currentCube">
        </component>
      </keep-alive>
    </div>
  </div>
</template>

<script>
  import Cube from './cube-details';
  import Dimensions from './cube-dimensions';
  import Facts from './cube-facts';

  export default {
    props: ['currentCube'],
    data: function () {
      return {
        // currentCube: this.currentCube,
        selectedComponent: 'appCube'
      }
    },
    components: {
      appCube: Cube,
      appDimensions: Dimensions,
      appFacts: Facts
    }
  }
</script>

<style scoped>

  .schema_props {
    position: relative;
    float: left;
    top: 30px;
    left: 25px;
    width: 800px;
    height: 480px;
    border: 1px solid #98a6ad;
    padding: 10px;

  }

  .cube_components {
    position: relative;
    float: top;
    padding: 5px;
    width: 100%;
    height: 40px;
    border: 1px solid #98a6ad;

  }

  button {
    margin-left: 5px
  }

</style>
