fixture `Logging user`
    .page `http://127.0.0.1:5000/login?next=%2Fdesigner`;
    // .httpAuth({
    //     username: 'admin',
    //     password: 'admin',
    // });

test('Test Login', async t => {
    await t
        .typeText('#username', 'admin')
        .typeText('#password', 'admin')
        .click('#submit');
});