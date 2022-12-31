import { Card, CardContent, Typography } from '@mui/material'
import { Image } from '../Styles'
import blank_img from '../images/blank_image.jpg'

type Props = {
    src: string
    caption?: string
}
const ImageCard = (props: Props) => {

    const caption = props.caption ? props.caption : 'Waiting for Upload...';
    const src = props.src ? props.src : blank_img;
    const cardStyles = {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
    }
    return (
        <Card sx={cardStyles}>
            <Image src={src} alt='uploaded' height='300px' />
            <CardContent sx={{alignItems: 'center', justifyContent: 'center'}}>
                <Typography variant='body2' fontFamily='cursive'>
                    {caption}
                </Typography>
            </CardContent>
        </Card>
    )

}

export default ImageCard