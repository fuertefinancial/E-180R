import { useState } from 'react'

function App() {
  const [emailContent, setEmailContent] = useState('')
  const [response, setResponse] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const generateResponse = async () => {
    if (!emailContent.trim()) {
      setError('Please enter an email to process')
      return
    }

    setLoading(true)
    setError('')
    setResponse('')

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const res = await fetch(`${apiUrl}/api/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email_content: emailContent }),
      })

      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`)
      }

      const data = await res.json()
      setResponse(data.response)
    } catch (err) {
      setError('Failed to generate response. Please try again.')
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Navigation Bar */}
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <h1 className="text-2xl font-bold text-gray-900">E-180R</h1>
            <p className="text-sm text-gray-600">AI-Powered Email Automation</p>
          </div>
      </div>
      </nav>

      {/* Main Content */}
      <div className="flex-1 flex">
        <div className="max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-full">
            {/* Email Input Section */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 flex flex-col">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                Incoming Email
              </h2>
              <textarea
                value={emailContent}
                onChange={(e) => setEmailContent(e.target.value)}
                placeholder="Paste the email content here..."
                className="flex-1 w-full p-4 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none font-mono text-sm"
              />
              <button
                onClick={generateResponse}
                disabled={loading}
                className="mt-4 bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors duration-200"
              >
                {loading ? 'Generating...' : 'Generate Response'}
        </button>
              {error && (
                <p className="mt-2 text-red-600 text-sm">{error}</p>
              )}
            </div>

            {/* Response Section */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 flex flex-col">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                Generated Response
              </h2>
              <div className="flex-1 w-full p-4 border border-gray-300 rounded-lg bg-gray-50 overflow-auto">
                {loading ? (
                  <div className="flex items-center justify-center h-full">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                  </div>
                ) : response ? (
                  <pre className="whitespace-pre-wrap font-sans text-sm text-gray-800">
                    {response}
                  </pre>
                ) : (
                  <p className="text-gray-500 text-center">
                    Generated response will appear here...
                  </p>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 py-4">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <p className="text-center text-sm text-gray-600">
            E-180R - Professional email responses powered by AI
          </p>
        </div>
      </footer>
    </div>
  )
}

export default App
