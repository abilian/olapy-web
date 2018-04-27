import { mount } from "vue-test-utils";
import schemaOptions from "@/cubes/base-schema-options";
import ConnectDB from "@/cubes/add_cube/connect-db";

describe("schemaOptions", () => {
  const wrapper = mount(schemaOptions);
  const vm = wrapper.vm;

  it("check base-schema-options data", () => {
    expect(vm.modalToShow).toBe("first");
    expect(vm.showModal).toBe(false);
    expect(vm.cube).toBe("");
    expect(vm.dbConfig).toBe("");
  });
});

describe("ConnectDB", () => {
  test("available databases", () => {
    const wrapper = mount(ConnectDB);
    let available_dbms = Array.apply(
      null,
      wrapper.find("select").element.options
    ).map(function(el) {
      return el.text;
    });
    expect(available_dbms).toEqual([
      "Choisissez",
      "Postgres",
      "Mysql",
      "Oracle",
      "SQL Server",
    ]);
  });
});
