import { Button } from '@mui/material'
import { useState } from 'react'
import { Container, Image } from '../Styles'

type Props = {
    text: string
}
const FileUploadButton = (props: Props) => {
    const [file, setFile] = useState('');

    function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
        if (!e.target.files) {
            return;
        }
        console.log(e.target.files);
        setFile(URL.createObjectURL(e.target.files[0]));
        console.log(file)
    }
    return (
        <Container>
            {file !== '' && <Image src={file} alt='uploaded' width='200px' />}
            <Button variant='contained' component='label'>
                {props.text}
                <input hidden type='file' accept='image/*' onChange={handleChange}/>
            </Button>
        </Container>
    )
}

export default FileUploadButton
