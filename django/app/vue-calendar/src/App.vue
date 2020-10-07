<template>
<body>
  <div id="nav">
    <Header />
    <router-view/>
    <Footer />
  </div>
</body>
</template>

<script>
import Header from './components/Header.vue'
import Footer from './components/Footer.vue'
export default {
  name: 'App',
  components: {
    Header,
    Footer
  }
};
</script>


<style>
* {
  margin: 0;
}
#app {
  text-align: center;
  color: #2c3e50;
}
</style>
