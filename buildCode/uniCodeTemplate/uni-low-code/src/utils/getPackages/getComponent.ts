import { shallowRef } from "vue";

export const loadComponent = async (com: string): Promise<any> => {
  try {
    const component = await import(`/src/packages/basic/${com}/index.vue`);
    return component.default;
  } catch (error) {
    console.error("Failed to load component:", error);
    return null;
  }
};

export const allLoadComponent = async (data: any): Promise<any> => {
  Promise.all(
    data.map(async (item: any) => {
      const component = await loadComponent(item.id.split("-")[0]);
      item.comName = shallowRef(component);
    })
  );
  return data;
};
