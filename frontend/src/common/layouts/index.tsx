import { Outlet } from "react-router-dom";
import MenuBar from "./menubar";
import Footer from "./footer";
import SignoutButton from "./siguout";
import { ToastContainer } from "react-toastify";

const Layout: React.FC = () => {
  return (
    <div className="flex flex-col min-h-screen">
      <div
        className="flex justify-between gap-1 p-4 text-white sticky top-0"
        style={{ backgroundColor: "#191919" }}
      >
        <MenuBar />
        <SignoutButton />
      </div>

      <div
        className="flex-grow bg-stone-800"
        style={{ backgroundColor: "#1C1C1C" }}
      >
        {/* */}
        <Outlet />
        <ToastContainer
          position="top-center"
          autoClose={3000}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
          theme="dark"
        />
      </div>
      <Footer />
    </div>
  );
};

export default Layout;
