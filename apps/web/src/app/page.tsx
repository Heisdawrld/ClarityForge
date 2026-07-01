import { ReasoningWorkspace } from "@/components/reasoning";

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50">
      <div className="container mx-auto py-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            ClarityForge
          </h1>
          <p className="text-gray-600">
            Your rigorous thinking partner. Audit biases, simulate outcomes, calibrate judgment.
          </p>
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          <div className="lg:col-span-3">
            <div className="bg-white rounded-lg shadow-lg overflow-hidden" style={{ height: "600px" }}>
              <ReasoningWorkspace />
            </div>
          </div>
          <div className="space-y-4">
            <div className="bg-white rounded-lg shadow p-4">
              <h2 className="font-semibold text-gray-900 mb-3">Quick Stats</h2>
              <div className="space-y-3">
                <div>
                  <p className="text-sm text-gray-500">Biases Detected</p>
                  <p className="text-2xl font-bold text-orange-600">3</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Confidence Score</p>
                  <p className="text-2xl font-bold text-green-600">78%</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Questions Answered</p>
                  <p className="text-2xl font-bold text-blue-600">2/5</p>
                </div>
              </div>
            </div>
            <div className="bg-white rounded-lg shadow p-4">
              <h2 className="font-semibold text-gray-900 mb-3">Recent Sessions</h2>
              <ul className="space-y-2">
                <li className="text-sm text-gray-600 hover:text-gray-900 cursor-pointer">
                  → Startup scaling strategy
                </li>
                <li className="text-sm text-gray-600 hover:text-gray-900 cursor-pointer">
                  → Market entry decision
                </li>
                <li className="text-sm text-gray-600 hover:text-gray-900 cursor-pointer">
                  → Team restructuring
                </li>
              </ul>
            </div>
            <div className="bg-white rounded-lg shadow p-4">
              <h2 className="font-semibold text-gray-900 mb-3">Calibration Score</h2>
              <div className="flex items-center justify-center">
                <div className="relative w-24 h-24">
                  <svg className="w-24 h-24 transform -rotate-90">
                    <circle
                      cx="48"
                      cy="48"
                      r="40"
                      stroke="#e5e7eb"
                      strokeWidth="8"
                      fill="none"
                    />
                    <circle
                      cx="48"
                      cy="48"
                      r="40"
                      stroke="#10b981"
                      strokeWidth="8"
                      fill="none"
                      strokeDasharray="251.2"
                      strokeDashoffset="75.36"
                      strokeLinecap="round"
                    />
                  </svg>
                  <span className="absolute inset-0 flex items-center justify-center text-xl font-bold text-green-600">
                    70%
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
