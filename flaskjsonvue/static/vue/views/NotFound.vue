<template>
    <h1>404</h1>
    <p>Page <mark>{{ $route.path }}</mark> was not found... <router-link :to="{ name: 'root' }">Home</router-link></p>
</template>
