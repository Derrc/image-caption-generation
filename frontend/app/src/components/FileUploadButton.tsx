import { Button } from '@mui/material'

type Props = {
    text: string
}
const FileUploadButton = (props: Props) => {
    return (
        <Button variant='contained' component='label'>
            {props.text}
            <input hidden type='file' accept='image/*' />
        </Button>
    )
}

export default FileUploadButton
