import { Button } from "@/components/ui/button"
import { Link } from "react-router-dom"

function LandingPage() {
  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <div className="flex flex-col items-center justify-center m-8">
        <h1 className="text-4xl font-bold">AI Venture</h1>
        <p className="text-lg text-gray-600">
          A strategy game where you build and lead AI labs to dominate the tech industry through smart investments and innovation.
        </p>
      </div>
      <div className="flex flex-row gap-4 items-center justify-center">
        <Button asChild>
          <Link to="/login">Login</Link>
        </Button>
        <Button asChild>
          <Link to="/register">Register</Link>
        </Button>
      </div>
    </div>
  )
}

export default LandingPage

