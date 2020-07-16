module.exports = {
  root: true,
  extends: [
    "eslint:recommended",
    "plugin:vue/essential",
    // "plugin:vue/strongly-recommended",

    // "@vue/prettier",
    // https://github.com/feross/standard/blob/master/RULES.md#javascript-standard-style
    "standard",
  ],
  plugins: [
    // required to lint *.vue files
    "vue",
    // "cypress",
  ],
  env: {
    es6: true,
    jest: true,
  },
  // add your custom rules here
  rules: {
    quotes: ["error", "double"],
    semi: ["error", "always"],
    "comma-dangle": ["error", "always-multiline"],
    "space-before-function-paren": ["error", "never"],
    // TODO fix this one
    "vue/no-use-v-if-with-v-for": 0,
  },
};
