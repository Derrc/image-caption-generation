import styled from 'styled-components'
import img from './images/sunflowers.jpg'

export const Container = styled.div`
    display: flex;
    height: 60%;
    flex-direction: column;
    justify-content: center;
    align-items: center;
`;

export const Background = styled.div`
    height: 1000px;
    background-image: url(${img});
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;
`

export const Text = styled.text`
    font-size: ${props => props.fontSize};
    font-weight: bold;
    color: #fff;
`

export const Image = styled.img`
    src: ${props => props.src};
    alt: ${props => props.alt};
    max-width: ${props => props.width};
    height: auto;
`


