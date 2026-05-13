   const handleVideoAnalysis = async (filename) => {
     setIsAnalyzing(true)
     setUploadError(null)
     
     try {
       const response = await api.post('/video/analyze', {
         filename: filename
       })
       
       if (response.data.success) {
         setAnalysisResults(response.data.analysis)
         alert('Video analysis completed!')
       } else {
         throw new Error(response.data.message || 'Analysis failed')
       }
     } catch (error) {
       console.error('Failed to analyze video:', error)
       setUploadError('Failed to analyze video: ' + (error.message || 'Unknown error'))
     } finally {
       setIsAnalyzing(false)
     }
   }