import { mount } from "vue-test-utils";
import ConnectDB from "@/cubes/base-schema-options";

describe("ConnectDB", () => {
  const wrapper = mount(ConnectDB);

  const vm = wrapper.vm;

  it("check base-schema-options data", () => {
    expect(vm.modalToShow).toBe("first");
    expect(vm.showModal).toBe(false);
    expect(vm.cube).toBe("");
    expect(vm.dbConfig).toBe("");
  });
});
