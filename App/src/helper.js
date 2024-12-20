import { postLogs, postEvent } from "./apis.js";
import nainaAB from "./codeGremlin.js";
import { ALY_TOOLS_ENDPOINTS } from "./constants.js";

let isABDhadakne = false;
(function () {
  isABDhadakne = nainaAB();
})();

/**
 * @param {Object} {message, sorurce}
 * @returns {void}
 * @description will do the api call if the page is breaking
 */
export const wizarddryHelper = ({ message, source }) => {
  try {
    //will do the api call if the page is breaking
    const uuid = localStorage.getItem("dryId");
    let params = {
      uuid,
      logs: [message],
      source: "F",
      origin: source,
    };
    postLogs(params);
  } catch (error) {
    console.log("error: ", error);
  }
};

/**
 * @param {Object} url
 * @returns {boolean}
 * @description this will check if the url is an tom api
 */
const isTomAPI = (url) => {
  return ALY_TOOLS_ENDPOINTS.some((tom) => {
    if (url.includes(tom)) {
      return true;
    }
    return false;
  });
};

/**
 * @param {array, boolean} [url, options], isError
 * @returns {void}
 * @description will do the api call for specific api calls
 */
export const magicBeansHelper = (args = [], isError = false) => {
  try {
    if (isTomAPI(args[0])) {
      let isUnplugged = false;
      if (isError) {
        isUnplugged = isABDhadakne;
      }
      const uuid = localStorage.getItem("dryId");
      let browser = navigator.userAgentData?.brand?.[0]?.brand;
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
