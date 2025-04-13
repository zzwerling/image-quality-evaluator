import ImgurSubmissionForm from './components/ImgurSubmissionForm';

export default function App() {
  return (

    <div className="min-h-screen flex flex-col items-center justify-start p-8 bg-gray-100">
    {/* Header */}
    <div className="text-center mb-10">
      <h1 className="text-4xl font-extrabold text-gray-900 flex items-center justify-center gap-2">
        🧠 <span>AI-Powered Photo Evaluator</span>
      </h1>
      <p className="text-gray-600 text-lg mt-2">
        Find out the quality of your photos using AI
      </p>
    </div>
  
    {/* Form */}
    <ImgurSubmissionForm />
  </div>
  );
}
