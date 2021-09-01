<template>
  <header>
    <img src="./assets/search.svg">
    <img src="./assets/add.svg">
    <img src="./assets/cards.svg">
  </header>
  
  <main>
  <router-view />
  </main>
  <footer></footer>
</template>

<script>

export default {
  name: 'App',
  components: {
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #294370;
}
header {
  position: absolute;
  display: flex;
  flex-direction: column;
  width: 40px;
  top: 64px;
  left: 20px;
}
header img {
  margin-bottom: 16px;
  cursor: pointer;
}
main {
  max-width: 800px;
  margin: 0 auto;
}
main h1 {
  text-align: center;
  margin: 160px 0 90px 0;
}
main p {
  line-height: 1.9;
  font-size: 18px;
  text-align: left;
}
main .card {
  margin: 40px 0;
  padding: 16px 24px;
  border-top-right-radius: 20px;
  border-bottom-left-radius: 20px;
  box-shadow: 0px 0px 20px 4px rgba(0,0,0,0.10);
}
main .card:hover {
  box-shadow: 0px 0px 20px 7px rgba(0,0,0,0.12);
}
</style>
