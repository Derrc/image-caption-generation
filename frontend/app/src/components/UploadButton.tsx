import { Button } from '@mui/material'
import { useEffect, useState } from 'react'
import { Container } from '../Styles'
import ImageCard from './ImageCard'

type Props = {
    text: string
}

const FileUploadButton = (props: Props) => {
    const [file, setFile] = useState('');
    const [caption, setCaption] = useState('')

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
    }

    // POST request sending image source and receiving caption after inference
    useEffect(() => {
        const requestOptions = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({source: file})
        }
        fetch(`/caption`, requestOptions).then(
            response => response.json()
        ).then(
          data => {
            setCaption(data)
          }
        )
      // run when dependencies change
      }, [file])

    return (
        <Container>
            {file && <ImageCard src={file} caption={caption} />}
            <Button sx={{marginTop: '20px'}} variant='contained' component='label'>
                {props.text}
                <input hidden type='file' accept='image/*' onChange={handleChange}/>
            </Button>
        </Container>
    )
}

export default FileUploadButton
