import { Card, CardContent, Typography } from '@mui/material'
import { Image } from '../Styles'

type Props = {
    src: string
    caption?: string
}
const ImageCard = (props: Props) => {

    const caption = props.caption ? props.caption : 'Generating Caption...';
    const cardStyles = {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
    }
    return (
        <Card sx={cardStyles}>
            <Image src={props.src} alt='uploaded' height='300px' />
            <CardContent sx={{alignItems: 'center', justifyContent: 'center'}}>
                <Typography variant='body2' fontFamily='cursive'>
                    {caption}
                </Typography>
            </CardContent>
        </Card>
    )

}

export default ImageCard