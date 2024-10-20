import { ThemeProvider } from "@/components/theme-provider"
import { Toaster } from "@/components/ui/sonner"
import { BrowserRouter as Router, Route, Routes } from "react-router-dom"
import LandingPage from "@/pages/LandingPage"
import LoginPage from "@/pages/LoginPage"
import RegisterPage from "@/pages/RegisterPage"
import VerifyPage from "@/pages/VerifyPage"
import PlayPage from "@/pages/PlayPage"
import { UserProvider } from "@/lib/stores/userStore"

function App() {
  return (
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <UserProvider>
        <div className="relative flex min-h-screen flex-col bg-background" id="page">
          {/* <SiteHeader /> */}
          <div className="flex-1">
            <Router>
              <Routes>
                <Route path="/" element={<LandingPage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route path="/verify" element={<VerifyPage />} />
                <Route path="/play" element={<PlayPage />} />
              </Routes>
            </Router>
          </div>
          {/* <SiteFooter /> */}
        </div>
        <Toaster richColors expand={true} />
      </UserProvider>
    </ThemeProvider>
  )
}

export default App
