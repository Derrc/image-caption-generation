import styled from 'styled-components'
import img from './images/bobross.jpg'

export const Container = styled.div`
    height: 775px;
    margin: -10px;
`
export const FlexContainer = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding-top: 50px;
`;

export const Background = styled.div`
    height: 100%;
    background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url(${img});
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;
`

export const Text = styled.text`
    font-size: ${props => props.fontSize};
    color: white;
    opacity: 0.9;
    font-family: cursive;
`

export const Image = styled.img`
    src: ${props => props.src};
    alt: ${props => props.alt};
    max-height: ${props => props.height};
    width: auto;
    border: solid;
    border-color: white;
    border-width: 5px;
`

export const cardStyles = {
    height: '100px',
    width: '100px',
}


