import { useState } from "react";
import axios from "axios";

function ImgurSubmissionForm() {
  const [imgURL, setimgURL] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);




  const options = new Map([
    ["Friendly & Simple", 0],
    ["Balanced Mode", 0.35],
    ["Bold & Playful", 0.7],
    ["Freestyle Mode", 1.0]
  ])
  

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResponse(null);

    try {
      const res = await axios.post("http://localhost:8000/evaluate", {
        "imgur_url": imgURL,
        "agreed_to_terms": true 
      });

      setResponse(res.data);
    } catch (err) {
      alert("Error calling backend");
    } finally {
      setLoading(false);
    }
  };

  return (
<div className="w-full max-w-md sm:max-w-lg md:max-w-xl mx-auto mt-10 bg-white shadow-xl rounded-xl p-6 sm:p-8 md:p-10">
<form onSubmit={handleSubmit} className="space-y-6">
        <h2 className="text-2xl font-bold text-black-800">Image Quality Tool</h2>
        <hr></hr>
        <h3 className="text-xl font-semibold text-gray-700 mb-1">Imgur Album Link: </h3>
        <h4 className="text-l font-semibold text-gray-700 mb-1">(note: only the first image will be used)</h4>
        <textarea
          className="w-full p-4 border border-gray-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
          rows="1"
          placeholder="Paste your imgur album link here: "
          value={imgURL}
          onChange={(e) => setimgURL(e.target.value)}
          maxLength={50}
          required
        />
  
        
  
        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-3 rounded-lg font-medium text-lg hover:bg-blue-700 transition"
          disabled={loading}
        >
          {loading ? "Analyzing..." : "Submit"}
        </button>
      </form>
  
      {response && (
        <div className="mt-10 border-t pt-6 space-y-4 text-sm text-gray-700">
          <div>
          <p className="text-lg mt-2">
  <strong className="text-blue-600">{response. score}/10</strong> — AI-rated photo quality
</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default ImgurSubmissionForm;