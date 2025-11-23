import React, { useContext } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import AuthContext from "./helpers/AuthContext";
import {
  Home,
  Login,
  Product,
  Register,
  Checkout,
  Policies,
  PaymentStatus,
  ForgotPassword,
  DeleteAccount,
  ProfilePictureUpload,
  UsersList,
  VulnTesting,
} from "./pages";
import { Loader, Navbar } from "./components";

const App = () => {
  const authCtx = useContext(AuthContext);
  if (!authCtx.isAuthChecked) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader />
      </div>
    );
  }

  return (
    <div className="flex flex-col min-h-screen md:h-screen p-4 md:p-8 text-primary">
      <Router>
        <Navbar />
        <Routes>
          <Route
            path="/login"
            element={!authCtx.isLoggedIn ? <Login /> : <Navigate to="/" />}
          />
          <Route
            path="/register"
            element={!authCtx.isLoggedIn ? <Register /> : <Navigate to="/" />}
          />
          <Route
            path="/forgot-password"
            element={<ForgotPassword />}
          />
          <Route
            path="/product/:id"
            element={
              <Product />
            }
          />
          <Route
            path="/checkout"
            element={
              authCtx.isLoggedIn ? <Checkout /> : <Navigate to="/login" />
            }
          />
          <Route path="/policies" element={<Policies />} />
          <Route
            path="/"
            element={
              <Home user={
                authCtx.isLoggedIn ? authCtx.user : null
              } />
            }
          />
          <Route
            path="/payment-status/:txnid"
            element={
              authCtx.isLoggedIn ? <PaymentStatus /> : <Navigate to="/login" />
            }
          />
          <Route
            path="/delete-account"
            element={
              authCtx.isLoggedIn ? <DeleteAccount /> : <Navigate to="/login" />
            }
          />
          <Route
            path="/profile-picture"
            element={
              authCtx.isLoggedIn ? <ProfilePictureUpload /> : <Navigate to="/login" />
            }
          />
          <Route
            path="/users"
            element={<UsersList />}
          />
          <Route
            path="/vuln-testing"
            element={<VulnTesting />}
          />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </Router>
    </div>
  );
};

export default App;

