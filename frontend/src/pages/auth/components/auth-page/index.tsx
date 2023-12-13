import React from "react";

// Update these imports according to your project structure
import { UserAuthForm } from "../user-auth-form";

const AuthenticationPage: React.FC = () => {
  return (
    <div className="container my-auto relative h-[400px] flex-col items-center justify-center flex">
      <UserAuthForm />
    </div>
  );
};

export default AuthenticationPage;
