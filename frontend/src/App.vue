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
          <v-text-field label="Video URL" :v-bind="url"></v-text-field>
        </v-col>
        <v-col>
          <v-combobox label="Person Name" :items="items" :v-bind="name"></v-combobox>
        </v-col>
        <v-col>
          <v-text-field label="Input Text" :v-bind="text"></v-text-field>
        </v-col>
        <v-col>
          <v-btn color="secondary" :loading="loading" @click="sendData()">Submit</v-btn>
        </v-col>
      </div>
      <v-col>
        <div class="bar_audio" :hidden="hidden">
          <audio controls>
            <source :src="filename">
            <!-- swap the id back to "player" and src= to id=-->
          </audio>
          <v-btn icon :hidden="hidden" :href="filename"><v-icon>mdi-download</v-icon></v-btn>
        </div>
      </v-col>
    </v-main>
  </v-app>
</template>

<script>

export default {
  name: 'App',

  data: () => ({
    items: ["Jesse Hartloff", "Andrew Hughes"],
    loading: false,
    filename: "",
    hidden: true,
    url: "",
    name: "",
    text: "",
    sendData: async function () {
      await this.ajaxPostRequest("path", "data", this.showData)
      this.loading = true
    },

    showData: async function (data) {
      this.hidden = false
      this.loading = false
      this.filename = data
      this.url = ""
      this.name = ""
      this.text = ""
    },

    ajaxPostRequest: async function (path, data, callback) {
      let request = new XMLHttpRequest();
      request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
          callback(this.response);
        }
      };
      request.open("POST", path);
      request.send(data);
    }
  }),
};
</script>
