import { Outlet } from "react-router-dom";
import MenuBar from "./menubar";
import Footer from "./footer";
import SignoutButton from "./siguout";

const Layout: React.FC = () => {
  return (
    <div className="flex flex-col min-h-screen">
      <div className="flex justify-between gap-1 p-4 text-white sticky top-0" style={{backgroundColor: "#191919"}}  >
        <MenuBar />
        <SignoutButton />
      </div>

      <div
        className="flex-grow bg-stone-800"
        style={{ backgroundColor: "#080202" }}
      >
        {/* */}
        <Outlet />
      </div>
      <Footer />
    </div>
  );
};

export default Layout;
