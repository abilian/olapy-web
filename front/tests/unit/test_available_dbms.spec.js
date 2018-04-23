import { mount } from "vue-test-utils";
import ConnectDB from "@/cubes/add_cube/connect-db";

describe("ConnectDB", () => {
  const wrapper = mount(ConnectDB);

  it("fait le rendu correctement", () => {
    expect(wrapper.html()).toContain(
      "<option>Postgres</option>" +
        "<option>Mysql</option>" +
        "<option>Oracle</option>" +
        "<option>SQL Server</option>"
    );
  });
});
