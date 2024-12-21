const BASE_URL = "http://localhost:8000/";

export const postLogs = (params) => {
  fetch(`${BASE_URL}log`, {
    method: "post",
    body: JSON.stringify(params),
    headers: {
      "Content-Type": "application/json",
    },
  }).catch((error) => {
    console.log("error: ", error);
  });
};

export const postEvent = (params) => {
  fetch(`${BASE_URL}event`, {
    method: "post",
    body: JSON.stringify(params),
    headers: {
      "Content-Type": "application/json",
    },
  }).catch((error) => {
    console.log("error: ", error);
  });
};
