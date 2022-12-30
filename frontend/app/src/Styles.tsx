import styled from 'styled-components'
import img from './images/sunflowers.jpg'

export const Container = styled.div`
    display: flex;
    height: 70%;
    flex-direction: column;
    justify-content: center;
    align-items: center;
`;

export const Background = styled.div`
    height: 1000px;
    background-image: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), url(${img});
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;
`

export const Text = styled.text`
    font-size: ${props => props.fontSize};
    font-weight: bold;
    color: white;
    opacity: 0.9;
`

export const Image = styled.img`
    src: ${props => props.src};
    alt: ${props => props.alt};
    max-height: ${props => props.height};
    width: auto;
`

export const cardStyles = {
    height: '100px',
    width: '100px',
}


