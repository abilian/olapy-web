import { Selector } from "testcafe";

fixture`Logging user`.page`http://127.0.0.1:5000/login?next=%2Fdesigner`;

test("Test Login", async t => {
  const username = Selector("#username");
  const password = Selector("#password");
  const loginBtn = Selector("#submit");

  await t
    .typeText(username, "admin")
    .typeText(password, "admin")
    .click(loginBtn);
  await t.expect(loginBtn.exists).notOk();
});
