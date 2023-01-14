import { HiPaperAirplane } from "react-icons/hi2";

function FlightCard({ data }) {
  return (
    <div className="py-6 px-4 max-w-md bg-gray-100 rounded-3xl shadow-xl">
      <div className="grid grid-cols-3 gap-4 place-items-center">
        <p className="col-span-3 mb-1 font-bold text-md">{data.start_date}</p>
        <p className="text-5xl font-extrabold">{data.start_airport}</p>
        <HiPaperAirplane size={40} />
        <p className="text-5xl font-extrabold">{data.end_airport}</p>
        <div className="flex flex-col items-center">
          <p className="text-xl">{data.start_time}</p>
          <p className="text-xs text-gray-400">{data.start_tz}</p>
        </div>
        <div className="flex justify-center items-center w-full">
          <hr className="w-full border-t-gray-400" />
          <p className="absolute px-3 text-gray-400 bg-gray-100 rounded-full border border-gray-400">{data.flight_duration}</p>
        </div>
        <div className="flex relative flex-col items-center">
          <p className="text-xl">{data.end_time}</p>
          <p className="text-xs text-gray-400">{data.end_tz}</p>
          {data.next_day && <p className="absolute -top-2 -right-5 text-sm font-medium text-gray-400">+1</p>}
        </div>
      </div>
    </div>
  );
}

export default FlightCard;
