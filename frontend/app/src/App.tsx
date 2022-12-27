import React, { useState, useEffect } from 'react'
import FileUploadButton from './components/FileUploadButton'

// placeholder type for passing data
type DataType = {
  // dictionary
  [key: string]: string[]
}

function App() {

  const [data, setData] = useState<DataType>({})

  const displayData = () => {
    if ('members' in data) {
      return (
        data.members.map((member, i) => (
          <p key={i}> {member} </p>
        ))
      )
    }
    return (
      <p> {'Loading...'} </p>
    )
  }

  useEffect(() => {
    fetch('/members').then(
      res => res.json()
    ).then(
      data => {
        setData(data)
        console.log(data)
      }
    )
  // only run on first render
  }, [])

  return (
    <div>
      {displayData()}
      <FileUploadButton text='Upload'/>
    </div>
  )
}

export default App