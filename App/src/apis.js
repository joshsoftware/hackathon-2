const API_ENDPOINT = "";

export const postLogs = (params) => {
  fetch(`${API_ENDPOINT}/log`, {
    method: "post",
    data: JSON.stringify(params),
  }).catch((error) => {
    console.log("error: ", error);
  });
};
