module.exports = {
  root: true,
  extends: [
    'plugin:vue/recommended',
    // 'plugin:vue/essential',
    // https://github.com/feross/standard/blob/master/RULES.md#javascript-standard-style
    'standard',
  ],
  // required to lint *.vue files
  plugins: [
    'html'
  ],
  env: {
    browser: true,
    es6: true,
    amd: true,
  },
  globals: {
    '$': true,
  },
  // add your custom rules here
  rules: {
    'quotes': 'off',
    'semi': ['error', 'always'],
    'comma-dangle': ['error', 'always-multiline'],
    'space-before-function-paren': 'off',
    'camelcase': 'off',

    // TODO
    'eqeqeq': 'off',
    'operator-linebreak': 'off',
  },
};
