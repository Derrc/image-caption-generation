import UploadButton from './components/UploadButton'
import { Container, Background, Text } from './Styles'

function App() {

  return (
      <Background>
        <Container>
          <Text fontSize='80px'> Image Caption Generator </Text>
          <UploadButton text='Upload'/>
        </Container>
      </Background>
  )
}

export default App