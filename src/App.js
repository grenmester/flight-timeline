import "./App.css";
import FlightCard from "./FlightCard";
import { IoAirplane } from "react-icons/io5";
import flights from "./data/flights";

function App() {
  return (
    <div className="bg-gray-200">
      <div className="flex flex-col items-center">
        <h1 className="my-10 text-6xl font-semibold">Flight Timeline</h1>
        <p className="mb-6 text-xl">There are {flights.length} recorded flights.</p>
        <ol className="border-l border-gray-700">
          {flights && flights.map(flight =>
            <li className="relative my-6 ml-8">
              <span className="flex absolute -left-12 top-20 justify-center items-center p-1.5 w-8 h-8 bg-gray-200 rounded-full ring-2 ring-gray-700">
                <IoAirplane className="text-gray-700" size={32} />
              </span>
              <FlightCard data={flight} />
            </li>
          )}
        </ol>
      </div>
      <div className="pb-24" />
    </div>
  );
}

export default App;
