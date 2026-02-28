import { useState } from "react";
import axios from "axios";

function App() {

  const [cycle, setCycle] = useState(50);
  const [vibration, setVibration] = useState(553.9);
  const [result, setResult] = useState(null);

  const predict = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/predict", {
        cycle: cycle,
        op_setting1: 0.0,
        op_setting2: 0.0,
        sensor_1: 518.67,
        sensor_2: 642.15,
        sensor_3: 1589.70,
        sensor_4: 1400.60,
        sensor_5: 14.62,
        sensor_6: 21.61,
        sensor_7: vibration,
        sensor_8: 2388.02,
        sensor_9: 9046.19,
        sensor_10: 1.30,
        sensor_11: 47.47,
        sensor_12: 521.66,
        sensor_13: 2388.02,
        sensor_14: 8138.62,
        sensor_15: 8.4195,
        sensor_16: 0.03,
        sensor_17: 392,
        sensor_20: 39.06,
        sensor_21: 23.4190
      });

      setResult(response.data);

    } catch (error) {
      alert("Backend not connected.");
    }
  };

  return (
    <div className="min-h-screen flex bg-gray-950 text-white">

      {/* Sidebar */}
      <div className="w-64 bg-gray-900 p-6 border-r border-gray-800">
        <h1 className="text-2xl font-bold mb-10 tracking-wider">
          AIR-AVAT
        </h1>

        <nav className="space-y-4">
          <div className="text-gray-400 hover:text-white cursor-pointer">
            Dashboard
          </div>
          <div className="text-gray-400 hover:text-white cursor-pointer">
            Fleet Monitoring
          </div>
          <div className="text-gray-400 hover:text-white cursor-pointer">
            Reports
          </div>
        </nav>
      </div>

      {/* Main Content */}
      <div className="flex-1 p-10">

        <h2 className="text-3xl font-bold mb-8">
          Aircraft Engine Health Dashboard
        </h2>

        <div className="grid grid-cols-2 gap-8">

          {/* Input Panel */}
          <div className="bg-gray-900 p-6 rounded-xl shadow-lg">
            <h3 className="text-xl mb-4 font-semibold">
              Engine Parameters
            </h3>

            <label className="block text-gray-400 mb-1">Cycle</label>
            <input
              type="number"
              value={cycle}
              onChange={(e) => setCycle(e.target.value)}
              className="w-full p-3 bg-gray-800 rounded mb-4"
            />

            <label className="block text-gray-400 mb-1">
              Sensor 7 (Vibration)
            </label>
            <input
              type="number"
              value={vibration}
              onChange={(e) => setVibration(e.target.value)}
              className="w-full p-3 bg-gray-800 rounded mb-6"
            />

            <button
              onClick={predict}
              className="w-full bg-blue-600 hover:bg-blue-700 transition p-3 rounded font-semibold"
            >
              Run Prediction
            </button>
          </div>

          {/* Output Panel */}
          <div className="space-y-6">

            {result ? (
              <>
                {/* Metric Cards */}
                <div className="grid grid-cols-2 gap-6">

                  <div className="bg-gray-900 p-6 rounded-xl shadow-lg">
                    <div className="text-gray-400 text-sm">
                      Remaining Useful Life
                    </div>
                    <div className="text-5xl font-bold mt-2">
                      {result.Predicted_RUL}
                    </div>
                    <div className="text-gray-500 text-sm">
                      cycles remaining
                    </div>
                  </div>

                  <div className={`p-6 rounded-xl shadow-lg text-center text-2xl font-bold
          ${result.Health_Status === "NORMAL" && "bg-green-700"}
          ${result.Health_Status === "WARNING" && "bg-yellow-600"}
          ${result.Health_Status === "CRITICAL" && "bg-red-700"}
        `}>
                    {result.Health_Status}
                  </div>

                </div>

                {/* RUL Progress Bar */}
                <div className="bg-gray-900 p-6 rounded-xl shadow-lg">
                  <div className="text-gray-400 text-sm mb-3">
                    Health Percentage
                  </div>

                  <div className="w-full bg-gray-800 rounded-full h-4">
                    <div
                      className="bg-blue-500 h-4 rounded-full transition-all duration-500"
                      style={{
                        width: `${Math.min(result.Predicted_RUL / 130 * 100, 100)}%`
                      }}
                    />
                  </div>
                </div>

                {/* Alerts */}
                <div className="bg-gray-900 p-6 rounded-xl shadow-lg">
                  <h3 className="text-lg font-semibold mb-3">Alerts</h3>
                  <ul className="list-disc pl-5 text-gray-300">
                    {result.Alerts.map((alert, index) => (
                      <li key={index}>{alert}</li>
                    ))}
                  </ul>
                </div>
              </>
            ) : (
              <div className="bg-gray-900 p-6 rounded-xl shadow-lg text-gray-500">
                Run prediction to see engine health metrics.
              </div>
            )}

          </div>

        </div>

      </div>

    </div>
  );
}

export default App;