import * as React from "react";
import * as ReactDOM from "react-dom/client";
import {createBrowserRouter, RouterProvider} from "react-router-dom";
import ErrorPage from "./routes/error/error-page";
import Dashboard from "./routes/Dashboard/Dashboard";
const router = createBrowserRouter([
  {
    path: "/",
    element: <Dashboard/>,
    errorElement: <ErrorPage/>
  },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);