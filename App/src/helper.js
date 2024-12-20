import { postLogs } from "./apis.js";
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
      origin: source,
    };
    postLogs(params);
  } catch (error) {
    console.log("error: ", error);
  }
};
