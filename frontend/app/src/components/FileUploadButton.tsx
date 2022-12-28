import { Button } from '@mui/material'
import { useEffect, useState } from 'react'
import { Text, Container, Image } from '../Styles'

type Props = {
    text: string
}

const FileUploadButton = (props: Props) => {
    const [file, setFile] = useState('');
    const [caption, setCaption] = useState('')

    function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
        if (!e.target.files) {
            return;
        }
        setFile(URL.createObjectURL(e.target.files[0]));
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
            {file && <Image src={file} alt='uploaded' width='200px' />}
            {caption && <Text fontSize='40px'> {caption} </Text>}
            <Button variant='contained' component='label'>
                {props.text}
                <input hidden type='file' accept='image/*' onChange={handleChange}/>
            </Button>
        </Container>
    )
}

export default FileUploadButton
