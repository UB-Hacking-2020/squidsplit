<template>
  <v-app>
    <v-app-bar
        app
        color="primary"
        dark
    >
      The Sentence GeneratorInator
      <v-spacer></v-spacer>

      <v-btn
          href="https://github.com/UB-Hacking-2020/squidsplit"
          target="_blank"
          text
      >
        <span class="mr-2">Source Code</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <div>
        <v-col>
          <v-text-field v-model="url" label="Video URL"></v-text-field>
        </v-col>
        <v-col>
          <v-combobox :items="items" v-model="name" disabled label="Person Name"></v-combobox>
        </v-col>
        <v-col>
          <v-text-field v-model="text" label="Input Text"></v-text-field>
        </v-col>
        <v-col>
          <v-btn :loading="loading" @click="sendData()" color="secondary">Submit</v-btn>
        </v-col>
      </div>
      <v-col>
        <div :hidden="hidden" class="bar_audio">
          <audio v-if="!loading" controls ref="audioplayer">
            <source :src="filename" >
            <!-- swap the id back to "player" and src= to id=-->
          </audio>
          <v-btn :hidden="hidden" :href="filename" icon>
            <v-icon>mdi-download</v-icon>
          </v-btn>
        </div>
      </v-col>
    </v-main>
  </v-app>
</template>

<script>
import axios from "axios";

export default {
  name: 'App',

  data: () => ({
    loading: false,
    filename: "",
    hidden: true,
    url: "",
    name: "",
    text: "",
    sendData: async function () {
      let data = {
        "url": this.url,
        "name": this.name,
        "text": this.text
      };
      data = JSON.stringify(data);
      axios.post("http://localhost:5000/request", data).then(response => {this.showData(response)});
      // this.loading = true;
    },

    showData: async function (data) {
      this.hidden = false;
      this.loading = false;
      this.filename = "http://localhost:5000/" + data.data;
      this.url = "";
      this.name = "";
      this.text = "";
      this.$refs.audioplayer.load();
    }
  }),
};
</script>
