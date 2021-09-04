import "./App.css";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Login from "./pages/Login";

function App() {
  const { token, login, logout, load, isToken, userId } = useAuth();
  let routes;

  if (token && userId === "investigator") {
    routes = (
      <Switch>
        <Route path="/" exact>
          <MainNavigation />
        </Route>
        <Route path="/investigator/signout" exact>
          <MainNavigation />
        </Route>
      </Switch>
    );
  } else if (token && userId === "incidentmanager") {
    routes = (
      <Switch>
        <Route path="/" exact>
          <MainNavigation />
        </Route>

        <Route path="/manager/signout" exact>
          <MainNavigation />
        </Route>
      </Switch>
    );
  } else if (token && userId === "admin") {
    routes = (
      <Switch>
        <Route path="/" exact>
          <MainNavigation />
        </Route>
        <Route path="/create-role" exact>
          <MainNavigation />
        </Route>
      </Switch>
    );
  } else if (!isToken) {
    routes = (
      <Switch>
        <Route path="/" exact>
          <Login />
        </Route>
        <Route path="/forgot" exact>
          <Forgot />
        </Route>
      </Switch>
    );
  } else if (isToken) {
    routes = (
      <Switch>
        <Route path="/" exact>
          <></>
        </Route>
      </Switch>
    );
  }

  return (
    <AuthContext.Provider
      value={{
        isLoggedIn: token,
        token: token,
        user: userId,
        payment: "",
        login: login,
        logout: logout,
      }}
    >
      <Router>
        <div>{load && <LoadingSpinner asOverlay />} </div>
        <div>{routes}</div>
      </Router>
    </AuthContext.Provider>
  );
}

export default App;
