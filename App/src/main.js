import "./wizarddry.js";

//generate the uuid for the user and store it in the local storage to identify the user
document.addEventListener("DOMContentLoaded", (event) => {
  function generateUUID() {
    return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function (c) {
      var r = (Math.random() * 16) | 0,
        v = c == "x" ? r : (r & 0x3) | 0x8;
      return v.toString(16);
    });
  }

  if (!localStorage.getItem("dryId")) {
    const uuid = generateUUID();
    localStorage.setItem("dryId", uuid);
  }
});
