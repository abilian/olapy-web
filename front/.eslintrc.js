module.exports = {
  root: true,
  // See: https://github.com/prettier/eslint-config-prettier
  extends: [
    "eslint:recommended",
    "plugin:vue/essential",
    "prettier",
    "prettier/standard",
    // "@vue/prettier",
    // "plugin:requirejs/recommended",
  ],
  // required to lint *.vue files
  plugins: ["vue"],
  env: {
    browser: true,
    es6: true,
    node: true,
  },
  // add your custom rules here
  rules: {
    semi: ["error", "always"],
    curly: "error",
    // TODO fix this one
    "vue/no-use-v-if-with-v-for": 0,
  },
};
