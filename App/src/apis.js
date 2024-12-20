const BASE_URL = "http://localhost:8000/";

export const postLogs = (params) => {
  fetch(`${BASE_URL}/log`, {
    method: "post",
    data: JSON.stringify(params),
  }).catch((error) => {
    console.log("error: ", error);
  });
};

export const postEvent = (params) => {
  fetch(`${BASE_URL}/event`, {
    method: "post",
    data: JSON.stringify(params),
  }).catch((error) => {
    console.log("error: ", error);
  });
};
