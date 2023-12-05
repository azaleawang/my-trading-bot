import { Outlet } from "react-router-dom";
import MenuBar from "./menubar";
import Footer from "./footer";

const Layout: React.FC = () => {
  return (
    <div className="flex flex-col min-h-screen">
      <MenuBar />
      <div className="flex-grow bg-stone-800" style={{"backgroundColor": "#080202"}}>
        {/* */}
        <Outlet />
      </div>
      <Footer />
    </div>
  );
};

export default Layout;
