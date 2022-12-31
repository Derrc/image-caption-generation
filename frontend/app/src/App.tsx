import UploadButton from './components/UploadButton'
import { Container, FlexContainer, Background, Text } from './Styles'

function App() {

  return (
    <Container>
      <Background>
        <FlexContainer>
          <Text fontSize={'50px'} > Image Caption Generator </Text>
          <Text fontSize={'20px'}> Upload an image to caption! </Text>
          <UploadButton text='Upload'/>
        </FlexContainer>
      </Background>
    </Container>
  )
}

export default App