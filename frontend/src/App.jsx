import { useState } from 'react'

function App() {
  const [recordA, setRecordA] = useState('{\n  "vendor": "Starbucks",\n  "amount": "$4.50",\n  "date": "2026-05-24"\n}')
  const [imageFile, setImageFile] = useState(null)
  const [imagePreview, setImagePreview] = useState(null)
  
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // Handle the file upload and create a preview URL
  const handleImageUpload = (e) => {
    const file = e.target.files[0]
    if (file) {
      setImageFile(file)
      setImagePreview(URL.createObjectURL(file))
    }
  }

  const handleReconcile = async () => {
    if (!imageFile) {
      setError("Please upload a receipt image first.")
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)
    
    try {
      // 1. Pack the text and the file into a FormData object
      const formData = new FormData()
      formData.append("record_a", recordA)
      formData.append("receipt_image", imageFile)

      // 2. Send it to our new vision endpoint (Note: Do NOT set Content-Type manually here)
      const response = await fetch('http://127.0.0.1:8000/api/reconcile-vision', {
        method: 'POST',
        body: formData
      })
      
      const data = await response.json()
      if (!response.ok) throw new Error(data.detail || "Server error")
      
      setResult(data)
    } catch (err) {
      setError(err.message)
    }
    
    setLoading(false)
  }

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto', padding: '40px', fontFamily: 'sans-serif' }}>
      <h2>Multimodal AI Reconciliation</h2>
      
      <div style={{ display: 'flex', gap: '20px', marginBottom: '20px' }}>
        
        {/* Left Side: The Database Record */}
        <div style={{ flex: 1 }}>
          <label><strong>Database Record (JSON)</strong></label>
          <textarea 
            value={recordA}
            onChange={(e) => setRecordA(e.target.value)}
            style={{ width: '100%', height: '250px', marginTop: '8px', fontFamily: 'monospace', padding: '10px' }}
          />
        </div>

        {/* Right Side: The Image Uploader */}
        <div style={{ flex: 1, border: '2px dashed #ccc', padding: '20px', textAlign: 'center', backgroundColor: '#fafafa' }}>
          <label style={{ display: 'block', marginBottom: '10px' }}><strong>Upload Physical Receipt</strong></label>
          <input type="file" accept="image/*" onChange={handleImageUpload} />
          
          {imagePreview && (
            <div style={{ marginTop: '15px' }}>
              <img src={imagePreview} alt="Receipt preview" style={{ maxHeight: '180px', borderRadius: '4px', border: '1px solid #ddd' }} />
            </div>
          )}
        </div>

      </div>

      <button 
        onClick={handleReconcile} 
        disabled={loading}
        style={{ width: '100%', padding: '12px', fontSize: '16px', cursor: 'pointer', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '4px' }}
      >
        {loading ? "AI is scanning image..." : "Compare Record with Image"}
      </button>

      {error && (
        <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#ffe6e6', color: '#cc0000', border: '1px solid #cc0000', borderRadius: '4px' }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {result && (
        <div style={{ marginTop: '20px', padding: '20px', backgroundColor: '#f8f9fa', border: '1px solid #dee2e6', borderRadius: '4px' }}>
          <h3 style={{ marginTop: 0 }}>Result: {result.is_match ? "✅ MATCH" : "❌ NO MATCH"}</h3>
          <p><strong>Confidence:</strong> {result.confidence_score}%</p>
          <p><strong>Explanation:</strong> {result.explanation}</p>
        </div>
      )}
    </div>
  )
}

export default App
