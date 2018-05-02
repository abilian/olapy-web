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

  const addCubeBtn = Selector("#show-modal");
  await t.click(addCubeBtn);

  const selectCubeSource = Selector("select");

  //https://testcafe-discuss.devexpress.com/t/how-can-i-select-a-dropdown-option/69/12
  await t.click(selectCubeSource).click(selectCubeSource.find("option").nth(2));

  const selectCubeEngine = Selector("#db-engine");
  // const servername = Selector("#servername");
  // const port = Selector("#port");
  // const user = Selector("#username");
  // const pass = Selector("#password");
  const showDatabasesBtn = Selector("#show-databases-btn");

  await t
    //by default, those variables are set
    // .typeText(servername, "localhost")
    // .typeText(port, "5432")
    // .typeText(user, "postgres")
    // .typeText(pass, "root")

    .click(selectCubeEngine)
    .click(selectCubeEngine.find("option").nth(1))
    .click(showDatabasesBtn)
    .expect(Selector("#available-databases").innerText)
    .contains("postgres");
});
