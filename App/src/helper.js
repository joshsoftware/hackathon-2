import { postLogs, postEvent } from "./apis.js";
import nainaAB from "./codeGremlin.js";
import { ALY_TOOLS_ENDPOINTS } from "./constants.js";

export const wizarddryHelper = ({ message, source }) => {
  try {
    const uuid = localStorage.getItem("dryId");
    let params = {
      uuid,
      log: String(message),
      source: "F",
      origin: source,
      title: "dummy",
      status: "PENDING"
    };
    postLogs(params);
  } catch (error) {
    console.log("error: ", error);
  }
};

const isTomAPI = (url) => {
  return ALY_TOOLS_ENDPOINTS.some((tom) => {
    if (url.includes(tom)) {
      return true;
    }
    return false;
  });
};

export const magicBeansHelper = async (args = [], isError = false) => {
  try {
    if (isTomAPI(args[0])) {
      let isUnplugged = false;
      if (isError) {
        isUnplugged = await nainaAB();
      };
      const uuid = localStorage.getItem("dryId");
      let browser = navigator.userAgentData?.brands?.[0]?.brand;
      let params = {
        uuid,
        url: args[0],
        source: "F",
        payload: args[1],
        ab_active: isUnplugged,
        user_agent: browser,
      };
      postEvent(params);
    }
  } catch (error) {
    console.log("error: ", error);
  }
};
