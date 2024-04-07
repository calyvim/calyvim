import Cookies from "js-cookie";
import axios from "axios";

const csrftoken = Cookies.get("csrftoken");

export const http = axios.create({
  baseURL: "/api",
  headers: {
    "X-CSRFToken": csrftoken,
  },
});
