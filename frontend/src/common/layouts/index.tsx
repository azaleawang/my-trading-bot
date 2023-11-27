import { Outlet } from "react-router-dom";
import MenuBar from "./menubar";
import Footer from "./footer";

const Layout: React.FC = () => {
  return (
    <>
      <MenuBar />
      <Outlet />
      <Footer />
    </>
  );
};

export default Layout;
