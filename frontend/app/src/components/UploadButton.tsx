import { Button } from '@mui/material'
import React, { useEffect, useState } from 'react'
import { FlexContainer } from '../Styles'
import ImageCard from './ImageCard'
import { useIsMount } from '../hooks'

type Props = {
    text: string
}

const FileUploadButton = (props: Props) => {
    const [file, setFile] = useState('');
    const [caption, setCaption] = useState('')

    // hook for actions after first render and after first render
    const isMount = useIsMount()

    // converts blobs to data urls for inference in backend
    function blobToDataURL(blob: Blob): Promise<void> {
        return new Promise<string>((resolve, reject) => {
          const reader = new FileReader();
          reader.onload = _e => resolve(reader.result as string);
          reader.onerror = _e => reject(reader.error);
          reader.onabort = _e => reject(new Error("Read aborted"));
          reader.readAsDataURL(blob);
        }).then(url => setFile(url))
      }

    function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
        if (!e.target.files) {
            return;
        }
        const blob = e.target.files[0]
        blobToDataURL(blob)
        setCaption('Generating Caption...')
    }

    function handleClick() {
      setCaption('Waiting for Upload...')
    }

    // POST request sending image source and receiving caption after inference
    useEffect(() => {
        const requestOptions = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({source: file})
        }
        // sends post requests after first render only
        if (!isMount) {
          fetch(`/caption`, requestOptions).then(
            response => response.json()
          ).then(
          data => {
            setCaption(data)
          }
        )
        }
      // run when dependencies change
      }, [file])

    return (
        <FlexContainer>
            <ImageCard src={file} caption={caption} />
            <Button sx={{marginTop: '20px', fontFamily:'cursive'}} variant='contained' component='label' color='inherit'>
                {props.text}
                <input hidden type='file' accept='image/*' onChange={handleChange} onClick={handleClick}/>
            </Button>
        </FlexContainer>
    )
}

export default FileUploadButton
